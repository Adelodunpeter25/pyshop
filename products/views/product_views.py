from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.cache import cache
from ..models import Product


def landing(request):
    featured_products = []
    for category in ['Footwears', 'Groceries', 'Electronics', 'Vehicles']:
        product = Product.objects.filter(category__iexact=category).exclude(image_url__isnull=True).exclude(image_url__exact='').first()
        if product:
            featured_products.append(product)
    return render(request, 'landing.html', {'featured_products': featured_products})


def all_products(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query) | Q(subcategory__icontains=query))
    
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
    
    sort_options = {'name': 'name', 'price_low': 'price', 'price_high': '-price', 'newest': '-id'}
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    categories = cache.get('product_categories')
    if not categories:
        categories = list(set(Product.objects.values_list('category', flat=True)))
        cache.set('product_categories', categories, 300)
    
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
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


def category_view(request, category_name):
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    subcategory = request.GET.get('subcategory', '')
    
    products = Product.objects.filter(category__iexact=category_name)
    
    if subcategory:
        products = products.filter(subcategory__iexact=subcategory)
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
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
    
    sort_options = {'name': 'name', 'price_low': 'price', 'price_high': '-price', 'newest': '-id'}
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'products': page_obj,
        'category': category_name,
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'is_paginated': page_obj.has_other_pages()
    }
    
    if category_name == 'Electronics':
        subcategories = list(set(Product.objects.filter(category__iexact='Electronics').exclude(subcategory__isnull=True).values_list('subcategory', flat=True)))
        context['subcategories'] = subcategories
        context['selected_subcategory'] = subcategory
    
    return render(request, 'index.html', context)


def groceries(request):
    return category_view(request, 'Groceries')


def footwears(request):
    return category_view(request, 'Footwears')


def vehicles(request):
    return category_view(request, 'Vehicles')


def electronics(request):
    return category_view(request, 'Electronics')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    recently_viewed = request.session.get('recently_viewed', [])
    if product_id not in recently_viewed:
        recently_viewed.insert(0, product_id)
        recently_viewed = recently_viewed[:10]
        request.session['recently_viewed'] = recently_viewed
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    
    return render(request, 'product_detail.html', {'product': product, 'related_products': related_products})
