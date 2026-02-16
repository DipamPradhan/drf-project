from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import (
    CursorPagination,
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Order, Product
from apis.serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
    OrderCreateSerializer,
)

from .filters import InStockFilterBackend, OrderFilter, ProductFilter

# @api_view(["GET"])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(
#         products,
#         many=True,
#     )

#     return Response(serializer.data)


# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "stock", "name"]
    pagination_class = LimitOffsetPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = "pagenumber"
    # pagination_class.page_size_query_param = "pagesize"
    # pagination_class.max_page_size = 5

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(["GET"])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(
#         product,
#     )

#     return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(["GET"])
# def order_list(request):
#     orders = Order.objects.prefetch_related(
#         "items__product",
#         "user",
#     )
#     serializer = OrderSerializer(
#         orders,
#         many=True,
#     )

#     return Response(serializer.data)


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items__product")
#     serializer_class = OrderSerializer


# # showing only registered USER data
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items__product")
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": products.count(),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )

        return Response(serializer.data)


# @api_view(["GET"])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer(
#         {
#             "products": products,
#             "count": products.count(),
#             "max_price": products.aggregate(max_price=Max("price"))["max_price"],
#         }
#     )

#     return Response(serializer.data)
