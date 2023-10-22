from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fashion', views.fashion, name='fashion'),
    path('electronic', views.electronic, name='electronic'),
    path('jewellery', views.jewellery, name='jewellery'),
    path('help_desk', views.help_desk, name='help_desk'),
    path('about_us', views.about_us, name='about_us'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/',
         views.remove_product_from_cart, name='remove_from_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('getCartItemCount/', views.get_cart_item_count,
         name='get_cart_item_count'),
 path('product/<int:product_id>/', views.product_details, name='product_details'),
]
