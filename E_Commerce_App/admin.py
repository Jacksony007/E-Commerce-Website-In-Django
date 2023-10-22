from django.contrib import admin
from .models import CustomUser, Category, Product, Order, OrderItem, Review, Cart, Wishlist, Payment

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Payment)
