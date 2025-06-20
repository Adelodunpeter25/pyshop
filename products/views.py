from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def landing(request):
    return render(request, 'landing.html')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products, 'category': 'All'})

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
    subcategories = ['Mobile Phone', 'Computer', 'Audio Devices']
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
