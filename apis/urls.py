from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductInfoAPIView,
    OrderListAPIView,
    UserOrderListAPIView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product_list"),
    path("products/info", ProductInfoAPIView.as_view(), name="product_info"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("orders/", OrderListAPIView.as_view(), name="order_list"),
    path("user-orders/", UserOrderListAPIView.as_view(), name="user_order_list"),
]
