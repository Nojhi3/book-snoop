from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# ✅ Custom User Model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="books_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="books_user_permissions", blank=True)
    
    def __str__(self):
        return self.username

# ✅ Book Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ✅ Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=9.99)  # 🔹 Increased max_digits
    stock = models.PositiveIntegerField(default=10)  
    cover_image = models.URLField(blank=True, null=True)  
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ✅ Review Model
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# ✅ Order Model (Now includes shipping details)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 🔹 Increased max_digits
    full_name = models.CharField(max_length=100, default="Your Name")
    address = models.TextField(default="Home")
    city = models.CharField(max_length=50, default="city")
    zip_code = models.CharField(max_length=10, default="00000")
    country = models.CharField(max_length=50, default="India")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed")],
        default="Pending"
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# ✅ Order Item Model (Decreases book stock)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=9.99)  # 🔹 Increased max_digits

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"

    def save(self, *args, **kwargs):
        """Reduce stock when an order item is created"""
        if self.book.stock >= self.quantity:
            self.book.stock -= self.quantity
            self.book.save()
        else:
            raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)
