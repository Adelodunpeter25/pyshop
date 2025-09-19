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
    from django.db.models import Case, When, IntegerField
    
    # Single optimized query to get one product per category
    categories = ['Footwears', 'Groceries', 'Electronics', 'Vehicles']
    
    featured_products = Product.objects.filter(
        category__in=categories
    ).exclude(
        image_url__isnull=True
    ).exclude(
        image_url__exact=''
    ).exclude(
        image_url__icontains='placeholder'
    ).exclude(
        name__iexact='Apple'  # Exclude broken Apple product
    ).exclude(
        name__icontains='Airpods'  # Exclude broken Airpods
    ).order_by(
        Case(
            When(category__iexact='Footwears', then=1),
            When(category__iexact='Groceries', then=2),
            When(category__iexact='Electronics', then=3),
            When(category__iexact='Vehicles', then=4),
            output_field=IntegerField()
        ),
        '-id'
    ).distinct('category')[:4]
    
    return render(request, 'landing.html', {'featured_products': featured_products})

def all_products(request):
    from django.core.cache import cache
    
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.select_related().all()
    
    # Search filtering
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(subcategory__icontains=query)
        )
    
    # Category filtering
    if category_filter:
        products = products.filter(category__iexact=category_filter)
    
    # Price filtering
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Sorting
    sort_options = {
        'name': 'name',
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-id'  # Use id instead of created_at for better performance
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Cache categories for 5 minutes
    categories = cache.get('product_categories')
    if not categories:
        categories = list(Product.objects.values_list('category', flat=True).distinct())
        cache.set('product_categories', categories, 300)
    
    # Add pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {
        'products': page_obj,
        'category': 'All', 
        'search_query': query,
        'categories': categories,
        'selected_category': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
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

@login_required
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
    """Enhanced user profile with dashboard features"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Get user's cart info
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    # Get recently viewed products (from session)
    recently_viewed = request.session.get('recently_viewed', [])
    recent_products = Product.objects.filter(id__in=recently_viewed[:5]) if recently_viewed else []
    
    context = {
        'profile': profile,
        'cart_count': cart_count,
        'recent_products': recent_products,
    }
    
    return render(request, 'profile.html', context)

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
    
    # Add to recently viewed
    recently_viewed = request.session.get('recently_viewed', [])
    if product_id not in recently_viewed:
        recently_viewed.insert(0, product_id)
        recently_viewed = recently_viewed[:10]  # Keep only last 10
        request.session['recently_viewed'] = recently_viewed
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:4]
    
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    product = get_object_or_404(Product, id=product_id)
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('product_detail', product_id=product_id)

def view_cart(request):
    cart = request.session.get('cart', {})
    if not cart:
        return render(request, 'cart.html', {
            'cart_items': [], 
            'cart_total': 0,
            'cart_count': 0
        })
    
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids).only('id', 'name', 'price', 'image_url')
    cart_items = []
    cart_total = 0
    cart_count = 0
    
    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = float(product.price) * quantity
        cart_total += item_total
        cart_count += quantity
        cart_items.append({
            'product': product, 
            'quantity': quantity, 
            'item_total': item_total
        })
    
    return render(request, 'cart.html', {
        'cart_items': cart_items, 
        'cart_total': cart_total,
        'cart_count': cart_count
    })

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
    """Helper function to get total items in cart"""
    cart = request.session.get('cart', {})
    return sum(cart.values())

@login_required
def admin_dashboard(request):
    """Admin dashboard with analytics"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('index')
    
    from django.db.models import Count, Avg
    
    # Basic stats
    total_products = Product.objects.count()
    total_users = Profile.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=10).count()
    
    # Category breakdown
    category_stats = Product.objects.values('category').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')
    
    # Recent products - use id instead of created_at for compatibility
    recent_products = Product.objects.order_by('-id')[:5]
    
    # Price analysis with safe defaults
    price_stats = {
        'avg_price': 0,
        'min_price': 0,
        'max_price': 0
    }
    
    if Product.objects.exists():
        price_agg = Product.objects.aggregate(avg_price=Avg('price'))
        price_stats['avg_price'] = price_agg['avg_price'] or 0
        
        min_product = Product.objects.order_by('price').first()
        max_product = Product.objects.order_by('-price').first()
        
        if min_product:
            price_stats['min_price'] = min_product.price
        if max_product:
            price_stats['max_price'] = max_product.price
    
    context = {
        'total_products': total_products,
        'total_users': total_users,
        'low_stock_products': low_stock_products,
        'category_stats': category_stats,
        'recent_products': recent_products,
        'price_stats': price_stats,
    }
    
    return render(request, 'admin_dashboard.html', context)
