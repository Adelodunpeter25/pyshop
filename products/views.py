from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Profile
from .forms import ProductForm, UserRegisterForm, ProfileForm

def index(request):
    products = Product.objects.all()[:20]  # Limit to 20 products for performance
    return render(request, 'index.html', {'products': products})

def landing(request):
    return render(request, 'landing.html')

def all_products(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    
    # Add pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {
        'products': page_obj,
        'category': 'All', 
        'search_query': query,
        'is_paginated': page_obj.has_other_pages()
    })

def groceries(request):
    products = Product.objects.filter(category__iexact='Groceries')
    return render(request, 'index.html', {'products': products, 'category': 'Groceries'})

def footwears(request):
    selected_category = request.GET.get('category', 'Footwears')
    if selected_category == 'All':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__iexact=selected_category)
    return render(request, 'footwears.html', {'products': products, 'category': selected_category})

def vehicles(request):
    products = Product.objects.filter(category__iexact='Vehicles')
    return render(request, 'index.html', {'products': products, 'category': 'Vehicles'})

def electronics(request):
    subcategory = request.GET.get('subcategory', '')
    products = Product.objects.filter(category__iexact='Electronics')
    if subcategory:
        products = products.filter(subcategory__iexact=subcategory)
    
    # Get subcategories dynamically from database
    subcategories = Product.objects.filter(
        category__iexact='Electronics'
    ).values_list('subcategory', flat=True).distinct().exclude(subcategory__isnull=True)
    
    return render(request, 'index.html', {
        'products': products,
        'category': 'Electronics',
        'subcategories': subcategories,
        'selected_subcategory': subcategory
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('footwears')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        product = get_object_or_404(Product, id=product_id)
        messages.success(request, f"{product.name} has been added to your cart.")
        return redirect('product_detail', product_id=product_id)
    return redirect('product_detail', product_id=product_id)

def view_cart(request):
    cart = request.session.get('cart', {})
    if not cart:
        return render(request, 'cart.html', {'cart_items': [], 'cart_total': 0})
    
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    cart_total = 0
    
    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = float(product.price) * quantity
        cart_total += item_total
        cart_items.append({
            'product': product, 
            'quantity': quantity, 
            'item_total': item_total
        })
    
    return render(request, 'cart.html', {
        'cart_items': cart_items, 
        'cart_total': cart_total
    })

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
    return redirect('view_cart')
