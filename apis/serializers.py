from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price"
    )

    # product = ProductSerializer(
    #     read_only=True,
    # )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            # "product",
            "quantity",
            "item_subtotal",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class OrderSerializer(serializers.ModelSerializer):
    # nested serializer
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "created_at",
            "user",
            "status",
            "items",
            "total_price",
        )


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(
        many=True,
        read_only=True,
    )

    count = serializers.IntegerField()
    max_price = serializers.FloatField()
