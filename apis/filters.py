import django_filters
from apis.models import Product
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        in_stock = request.query_params.get("in_stock")
        if in_stock is not None:
            if in_stock.lower() == "true":
                return queryset.filter(stock__gt=0)
            elif in_stock.lower() == "false":
                return queryset.filter(stock=0)
        return queryset


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "icontains"],
            "price": ["exact", "lt", "gt", "range"],
        }
