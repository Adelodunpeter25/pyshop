from django.contrib import admin
from .models import Product, Offer
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'price', 'stock', 'category', 'subcategory')
    search_fields = ('name', 'category', 'subcategory', 'description')


class OfferAdmin(admin.ModelAdmin):
    list_display = ("code", "discount")


admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
