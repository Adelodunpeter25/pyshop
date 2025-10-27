from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import F
from ..forms import UserRegisterForm
from ..models import Cart, CartItem, Product


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


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            _migrate_session_cart_to_db(request)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            _migrate_session_cart_to_db(request)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
