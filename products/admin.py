from django.contrib import admin
from .models import Product, Offer, Profile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'subcategory')
    search_fields = ('name', 'category', 'subcategory', 'description')
    list_filter = ('category', 'subcategory')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_active', 'expires_at')
    list_filter = ('is_active',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country')
    search_fields = ('user__username', 'user__email')
