from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F
from ..models import Product, Cart, CartItem


def _migrate_session_cart_to_db(request):
    """Migrate session cart to database cart when user logs in"""
    if not request.user.is_authenticated:
        return
    
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    for product_id, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity = F('quantity') + quantity
                cart_item.save()
                cart_item.refresh_from_db()
        except Product.DoesNotExist:
            continue
    
    # Clear session cart after migration
    request.session['cart'] = {}
    request.session.modified = True


@require_POST
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your cart.")
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    
    # Check stock availability
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f"Sorry, only {product.stock} units of {product.name} are available.")
            return redirect('product_detail', product_id=product_id)
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
        cart_item.refresh_from_db()
    
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('product_detail', product_id=product_id)


def view_cart(request):
    if not request.user.is_authenticated:
        # Show session cart for anonymous users
        cart = request.session.get('cart', {})
        if not cart:
            return render(request, 'cart.html', {'cart_items': [], 'cart_total': 0, 'cart_count': 0})
        
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        cart_total = 0
        cart_count = 0
        
        for product in products:
            quantity = cart.get(str(product.id), 0)
            item_total = float(product.price) * quantity
            cart_total += item_total
            cart_count += quantity
            cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
        
        return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total, 'cart_count': cart_count})
    
    # Migrate session cart if exists
    _migrate_session_cart_to_db(request)
    
    # Get database cart for authenticated users
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return render(request, 'cart.html', {'cart_items': [], 'cart_total': 0, 'cart_count': 0})
    
    cart_items = []
    cart_total = 0
    cart_count = 0
    
    for cart_item in cart.items.select_related('product').all():
        item_total = float(cart_item.product.price) * cart_item.quantity
        cart_total += item_total
        cart_count += cart_item.quantity
        cart_items.append({
            'product': cart_item.product,
            'quantity': cart_item.quantity,
            'item_total': item_total
        })
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total, 'cart_count': cart_count})


@require_POST
def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
        return redirect('view_cart')
    
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


@require_POST
def update_cart_quantity(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        
        if quantity > 0:
            cart[str(product_id)] = quantity
            messages.success(request, "Cart updated successfully.")
        else:
            cart.pop(str(product_id), None)
            messages.success(request, "Item removed from cart.")
        
        request.session['cart'] = cart
        return redirect('view_cart')
    
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        if quantity > 0:
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                # Check stock availability
                product = cart_item.product
                if quantity > product.stock:
                    messages.warning(request, f"Sorry, only {product.stock} units available.")
                    return redirect('view_cart')
                
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully.")
        else:
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
            messages.success(request, "Item removed from cart.")
    
    return redirect('view_cart')


def get_cart_count(request):
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        return JsonResponse({'count': sum(cart.values())})
    
    # Migrate session cart if exists
    _migrate_session_cart_to_db(request)
    
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({'count': 0})
    
    count = sum(item.quantity for item in cart.items.all())
    return JsonResponse({'count': count})
