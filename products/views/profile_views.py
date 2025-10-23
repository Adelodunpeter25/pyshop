from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from ..models import Product, Profile
from ..forms import ProfileForm, ProductForm


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
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
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'edit_profile.html', {'form': form})


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


@require_POST
def clear_recently_viewed(request):
    request.session['recently_viewed'] = []
    return JsonResponse({'success': True})
