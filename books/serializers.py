from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Category, Review, Order, OrderItem

User = get_user_model()  # ✅ Use the custom User model

# ✅ Register Serializer (Ensures password is hashed)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        """Creates a new user with hashed password"""
        user = User.objects.create_user(**validated_data)
        return user

# ✅ User Serializer (Uses `is_staff` instead of `is_admin`)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]

# ✅ Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# ✅ Book Serializer (Now allows updates)
class BookSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # 🔹 Allows updating category by ID

    class Meta:
        model = Book
        fields = "__all__"

# ✅ Review Serializer (Includes user details)
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"

# ✅ OrderItem Serializer (Uses book ID instead of nested object)
class OrderItemSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # 🔹 Allows selecting book by ID

    class Meta:
        model = OrderItem
        fields = ["id", "book", "quantity", "price"]

# ✅ Order Serializer (Allows creating orders)
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True)  # 🔹 Supports multiple order items

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        """Creates an order and associated order items"""
        items_data = validated_data.pop("items")  # Get order items
        order = Order.objects.create(**validated_data)  # Create order

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)  # Create order items

        return order
