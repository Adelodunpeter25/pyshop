from django.urls import path
from . import views


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
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('clear-recently-viewed/', views.clear_recently_viewed, name='clear_recently_viewed'),
]