from django.urls import path
from .views import order_list, product_list, product_detail

urlpatterns = [
    path("products/", product_list, name="product_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("orders/", order_list, name="order_list"),
]
