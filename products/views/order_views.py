from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from ..models import Product, Profile, Order, OrderItem
import secrets


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')
    
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    cart_total = 0
    
    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = float(product.price) * quantity
        cart_total += item_total
        cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    
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
        
        request.session['cart'] = {}
        return redirect('payment', order_id=order.id)
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total, 'profile': profile})


@login_required
def payment(request, order_id):
    from django.conf import settings
    
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
    from django.conf import settings
    from pypaystack2 import Transaction
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    reference = request.POST.get('reference')
    
    if not reference:
        return JsonResponse({'success': False, 'message': 'No reference provided'})
    
    try:
        transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
        response = transaction.verify(reference=reference)
        
        if response['status'] and response['data']['status'] == 'success':
            order.status = 'paid'
            order.save()
            
            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            return JsonResponse({'success': True, 'message': 'Payment verified'})
        else:
            return JsonResponse({'success': False, 'message': 'Payment verification failed'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})
