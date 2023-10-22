from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from django.core.validators import MaxValueValidator, MinValueValidator

# Enumeration for User Types
class UserType(Enum):
    ADMIN = 'admin'
    STAFF = 'staff'
    CUSTOMER = 'customer'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    user_type = models.CharField(
        max_length=10, choices=UserType.choices(), default=UserType.CUSTOMER.value)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# Model representing Product Categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Model representing individual products
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

# Model representing user orders
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_details = models.TextField()
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

# Model representing individual items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity}) in Order #{self.order.pk}"

# Model for product reviews by users
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating from 1 to 5
    review_text = models.TextField()

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username} - Rating: {self.rating}"

# Model representing user carts
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name} (Qty: {self.quantity})"

# Model representing user wishlists
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s Wishlist"

# Model representing order payments
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    transaction_details = models.TextField()

    def __str__(self):
        return f"Payment for Order #{self.order.pk} via {self.payment_method}"
