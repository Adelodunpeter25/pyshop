from django.urls import path
from . import views
from . import views_site


urlpatterns = [
    path('', views.landing, name='landing'),
    path('all/', views.all_products, name='all_products'),
    path('groceries/', views.groceries, name='groceries'),
    path('footwears/', views.footwears, name='footwears'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('electronics/', views.electronics, name='electronics'),
    path('add-product/', views.add_product, name='add_product'),
]