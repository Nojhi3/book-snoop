from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, BookViewSet, CategoryViewSet, ReviewViewSet, OrderViewSet, OrderItemViewSet, 
    login_view, logout_view, register_view, home_view, book_detail_view, book_list_view, 
    cart_view, add_to_cart, remove_from_cart, clear_cart, checkout_view, order_success, add_review
)
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# ✅ API Router for DRF
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

# ✅ Web Pages (Frontend)
urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
    path('books/', book_list_view, name='book_list'),
    path('books/<int:book_id>/', book_detail_view, name='book_detail'),
    path("books/<int:book_id>/review/", add_review, name="add_review"),

    
    # ✅ Shopping Cart
    path('cart/', cart_view, name='cart_detail'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),

    # ✅ Checkout & Orders
    path('checkout/', checkout_view, name='checkout'),
    path('order-success/', order_success, name='order_success'),
]

# ✅ API Endpoints (DRF)
urlpatterns += [
    path('api/', include(router.urls)),  # Includes all API ViewSets

    # ✅ API Authentication
    path('api/auth/login/', login_view, name='api_login'),
    path('api/auth/logout/', logout_view, name='api_logout'),
    path('api/auth/register/', register_view, name='api_register'),

    # ✅ Password Reset (For Web Users)
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
