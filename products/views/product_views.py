from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, IntegerField
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from ..models import Product
from ..forms import ProductForm


def index(request):
    products = Product.objects.all()[:20]
    return render(request, 'index.html', {'products': products})


def landing(request):
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
        name__iexact='Apple'
    ).exclude(
        name__icontains='Airpods'
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
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.select_related().all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(subcategory__icontains=query)
        )
    
    if category_filter:
        products = products.filter(category__iexact=category_filter)
    
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
    
    sort_options = {
        'name': 'name',
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-id'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    categories = cache.get('product_categories')
    if not categories:
        categories = list(Product.objects.values_list('category', flat=True).distinct())
        cache.set('product_categories', categories, 300)
    
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
    
    subcategories = Product.objects.filter(
        category__iexact='Electronics'
    ).values_list('subcategory', flat=True).distinct().exclude(subcategory__isnull=True)
    
    return render(request, 'index.html', {
        'products': products,
        'category': 'Electronics',
        'subcategories': subcategories,
        'selected_subcategory': subcategory
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    recently_viewed = request.session.get('recently_viewed', [])
    if product_id not in recently_viewed:
        recently_viewed.insert(0, product_id)
        recently_viewed = recently_viewed[:10]
        request.session['recently_viewed'] = recently_viewed
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:4]
    
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
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