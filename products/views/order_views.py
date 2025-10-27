from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from ..models import Product, Profile, Order, OrderItem, Cart, CartItem
import secrets
import hmac
import hashlib
import json


def _get_cart_items(request):
    """Helper function to get cart items for both session and DB carts"""
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        if not cart:
            return [], 0
        
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        cart_total = 0
        
        for product in products:
            quantity = cart.get(str(product.id), 0)
            item_total = float(product.price) * quantity
            cart_total += item_total
            cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
        
        return cart_items, cart_total
    
    # Get database cart for authenticated users
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return [], 0
    
    cart_items = []
    cart_total = 0
    
    for cart_item in cart.items.select_related('product').all():
        item_total = float(cart_item.product.price) * cart_item.quantity
        cart_total += item_total
        cart_items.append({
            'product': cart_item.product,
            'quantity': cart_item.quantity,
            'item_total': item_total
        })
    
    return cart_items, cart_total


def _clear_cart(request):
    """Helper function to clear cart after checkout"""
    if not request.user.is_authenticated:
        request.session['cart'] = {}
        return
    
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()


@login_required
def checkout(request):
    cart_items, cart_total = _get_cart_items(request)
    
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')
    
    # Check stock availability
    for item in cart_items:
        if item['quantity'] > item['product'].stock:
            messages.error(request, f"Sorry, only {item['product'].stock} units of {item['product'].name} are available.")
            return redirect('view_cart')
    
    profile = Profile.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        reference = f"PS-{secrets.token_hex(8).upper()}"
        
        order = Order.objects.create(
            user=request.user,
            reference=reference,
            total_amount=cart_total,
            shipping_address=request.POST.get('address', profile.address if profile else ''),
            shipping_city=request.POST.get('city', profile.city if profile else ''),
            shipping_country=request.POST.get('country', profile.country if profile else ''),
            phone=request.POST.get('phone', profile.phone if profile else ''),
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        
        _clear_cart(request)
        return redirect('payment', order_id=order.id)
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total, 'profile': profile})


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.info(request, "This order has already been processed.")
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount_in_kobo': int(order.total_amount * 100),
    }
    return render(request, 'payment.html', context)


@require_POST
def verify_payment(request, order_id):
    """Manual payment verification (fallback)"""
    from pypaystack2 import Transaction
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    reference = request.POST.get('reference')
    
    if not reference:
        return JsonResponse({'success': False, 'message': 'No reference provided'})
    
    try:
        transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
        response = transaction.verify(reference=reference)
        
        if response['status'] and response['data']['status'] == 'success':
            # Only update if not already paid (webhook might have processed it)
            if order.status == 'pending':
                order.status = 'paid'
                order.save()
                
                for item in order.items.all():
                    product = item.product
                    if product.stock >= item.quantity:
                        product.stock -= item.quantity
                        product.save()
            
            return JsonResponse({'success': True, 'message': 'Payment verified'})
        else:
            return JsonResponse({'success': False, 'message': 'Payment verification failed'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_POST
def paystack_webhook(request):
    """Handle Paystack webhook events"""
    # Verify webhook signature
    paystack_signature = request.headers.get('X-Paystack-Signature', '')
    
    if not paystack_signature:
        return HttpResponse(status=400)
    
    # Compute HMAC signature
    secret_key = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
    body = request.body
    computed_signature = hmac.new(secret_key, body, hashlib.sha512).hexdigest()
    
    if not hmac.compare_digest(computed_signature, paystack_signature):
        return HttpResponse(status=400)
    
    # Parse webhook data
    try:
        data = json.loads(body.decode('utf-8'))
        event = data.get('event')
        event_data = data.get('data', {})
        
        if event == 'charge.success':
            reference = event_data.get('reference')
            status = event_data.get('status')
            
            if status == 'success' and reference:
                # Find order by reference
                try:
                    order = Order.objects.get(reference=reference)
                    
                    # Only process if order is still pending
                    if order.status == 'pending':
                        order.status = 'paid'
                        order.save()
                        
                        # Reduce stock
                        for item in order.items.all():
                            product = item.product
                            if product.stock >= item.quantity:
                                product.stock -= item.quantity
                                product.save()
                        
                        # Log successful webhook processing
                        print(f"Webhook processed: Order {reference} marked as paid")
                
                except Order.DoesNotExist:
                    print(f"Order not found for reference: {reference}")
        
        return HttpResponse(status=200)
    
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return HttpResponse(status=500)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})
