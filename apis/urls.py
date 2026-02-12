from django.urls import path
from .views import product_info, order_list, product_list, product_detail

urlpatterns = [
    path("products/", product_list, name="product_list"),
    path("products/info", product_info, name="product_info"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("orders/", order_list, name="order_list"),
]
