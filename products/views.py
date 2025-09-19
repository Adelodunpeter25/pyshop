from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
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
    # Get one product from each category
    featured_products = []
    
    footwears = Product.objects.filter(category__iexact='Footwears').exclude(image_url__isnull=True).exclude(image_url__exact='').first()
    if footwears:
        featured_products.append(footwears)
        
    groceries = Product.objects.filter(category__iexact='Groceries').exclude(image_url__isnull=True).exclude(image_url__exact='').first()
    if groceries:
        featured_products.append(groceries)
        
    electronics = Product.objects.filter(category__iexact='Electronics').exclude(image_url__isnull=True).exclude(image_url__exact='').first()
    if electronics:
        featured_products.append(electronics)
        
    vehicles = Product.objects.filter(category__iexact='Vehicles').exclude(image_url__isnull=True).exclude(image_url__exact='').first()
    if vehicles:
        featured_products.append(vehicles)
    
    return render(request, 'landing.html', {'featured_products': featured_products})

def all_products(request):
    from django.core.cache import cache
    
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.all()
    
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
        'newest': '-id'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Cache categories for 5 minutes
    categories = cache.get('product_categories')
    if not categories:
        categories = list(set(Product.objects.values_list('category', flat=True)))
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
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(category__iexact='Groceries')
    
    # Search filtering
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
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
        'newest': '-id'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Add pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {
        'products': page_obj,
        'category': 'Groceries',
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'is_paginated': page_obj.has_other_pages()
    })

def footwears(request):
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(category__iexact='Footwears')
    
    # Search filtering
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
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
        'newest': '-id'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Add pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {
        'products': page_obj,
        'category': 'Footwears',
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'is_paginated': page_obj.has_other_pages()
    })

def vehicles(request):
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(category__iexact='Vehicles')
    
    # Search filtering
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
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
        'newest': '-id'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Add pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {
        'products': page_obj,
        'category': 'Vehicles',
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'is_paginated': page_obj.has_other_pages()
    })

def electronics(request):
    query = request.GET.get('q', '').strip()
    subcategory = request.GET.get('subcategory', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(category__iexact='Electronics')
    if subcategory:
        products = products.filter(subcategory__iexact=subcategory)
    
    # Search filtering
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(subcategory__icontains=query)
        )
    
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
        'newest': '-id'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Get subcategories dynamically from database
    subcategories = list(set(Product.objects.filter(
        category__iexact='Electronics'
    ).exclude(subcategory__isnull=True).values_list('subcategory', flat=True)))
    
    # Add pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {
        'products': page_obj,
        'category': 'Electronics',
        'subcategories': subcategories,
        'selected_subcategory': subcategory,
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'is_paginated': page_obj.has_other_pages()
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
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            # Save user fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            # Save profile
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
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
        return render(request, 'cart.html', {
            'cart_items': [], 
            'cart_total': 0,
            'cart_count': 0
        })
    
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

def get_cart_count(request):
    """AJAX endpoint to get current cart count"""
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return JsonResponse({'count': count})

@require_POST
def clear_recently_viewed(request):
    """Clear recently viewed products from session"""
    request.session['recently_viewed'] = []
    return JsonResponse({'success': True})
