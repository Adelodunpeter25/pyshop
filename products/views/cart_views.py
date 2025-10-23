from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from ..models import Product


@require_POST
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your cart.")
        return redirect('login')
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    product = get_object_or_404(Product, id=product_id)
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('product_detail', product_id=product_id)


def view_cart(request):
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


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


@require_POST
def update_cart_quantity(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    
    if quantity > 0:
        cart[str(product_id)] = quantity
        messages.success(request, "Cart updated successfully.")
    else:
        cart.pop(str(product_id), None)
        messages.success(request, "Item removed from cart.")
    
    request.session['cart'] = cart
    return redirect('view_cart')


def get_cart_count(request):
    cart = request.session.get('cart', {})
    return JsonResponse({'count': sum(cart.values())})
