from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    product_info,
    OrderListAPIView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product_list"),
    path("products/info", product_info, name="product_info"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("orders/", OrderListAPIView.as_view(), name="order_list"),
]
