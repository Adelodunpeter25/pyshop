from django.urls import path
from . import views
from . import views_site


urlpatterns = [
    path('', views.landing, name='landing'),
    path('all/', views.all_products, name='all_products'),
    path('groceries/', views.groceries, name='groceries'),
    path('footwears/', views.footwears, name='footwears'),
    path('update-site-name/', views_site.update_site_name, name='update_site_name'),
    path('add-product/', views.add_product, name='add_product'),
]