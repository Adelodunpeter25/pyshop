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
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]