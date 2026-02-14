from django.urls import path
from .views import (
    OrderViewSet,
    ProductDetailAPIView,
    ProductInfoAPIView,
    ProductListCreateAPIView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="product_list"),
    path("products/info", ProductInfoAPIView.as_view(), name="product_info"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
]

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
urlpatterns += router.urls
