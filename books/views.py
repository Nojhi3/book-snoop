
from rest_framework import viewsets, permissions, status, views
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from books.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_POST


from .models import User, Book, Category, Review, Order, OrderItem
from .serializers import UserSerializer, BookSerializer, CategorySerializer, ReviewSerializer, OrderSerializer, OrderItemSerializer, RegisterSerializer
from .permissions import IsAdminUser
from .cart import Cart
from .forms import CheckoutForm, CustomUserCreationForm


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)  # Django's session-based login
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Logout View
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)  # Django's session-based logout
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

def home_view(request):
    return render(request, "home.html")

def book_list_view(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

def book_detail_view(request, book_id):
    """Display book details along with its reviews"""
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()  # ✅ Fetch all reviews related to the book

    return render(request, "books/book_detail.html", {"book": book, "reviews": reviews})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, "auth/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect(request.GET.get("next", "home"))  # 🔹 Redirect to checkout if needed
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})

@require_POST  # 🔹 Only allow POST requests for security
def logout_view(request):
    """Logs out the user and redirects to the homepage."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


def book_list_view(request):
    query = request.GET.get("q", "")  # Get the search query from URL
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)  # Case-insensitive search
    
    return render(request, "books/book_list.html", {"books": books, "query": query})

def cart_view(request):
    """Returns cart details as JSON."""
    cart = Cart(request)
    # cart_items = list(cart)  # Convert generator to list

    # return JsonResponse({"cart": cart_items, "total_price": float(cart.get_total_price())})
    return render(request, "cart/cart_detail.html", {"cart": cart})

def add_to_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book)
    return redirect("cart_detail")

def remove_from_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect("cart_detail")

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="login")  
def checkout_view(request):
    """Handle checkout process"""
    cart = Cart(request)

    if not cart.cart:  # Check if cart is empty
        messages.error(request, "Your cart is empty. Add items before checkout.")
        return redirect("cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=cart.get_total_price(),
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=Book.objects.get(id=item["book"]["id"]),  # Ensure correct book reference
                    quantity=item["quantity"],
                    price=item["total_price"] / item["quantity"]
                )
            cart.clear()  # Empty cart after checkout
            messages.success(request, "Order placed successfully!")
            return redirect("order_success")
    else:
        form = CheckoutForm()

    return render(request, "checkout/checkout.html", {"form": form, "cart": cart})

def order_success(request):
    return render(request, "checkout/order_success.html")

def add_review(request, book_id):
    """Handle review submission"""
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating and comment:
            Review.objects.create(book=book, user=request.user, rating=int(rating), comment=comment)
            messages.success(request, "Review added successfully!")
        else:
            messages.error(request, "All fields are required.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]  # Only admins can modify categories
        return [permissions.AllowAny()]  # Everyone can view categories

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """Only allow admins to modify books"""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [permissions.AllowAny()]  # Everyone can view books

# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # Everyone can view orders
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """Return orders belonging to the logged-in user"""
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# OrderItem ViewSet
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

