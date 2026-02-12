from django.http import JsonResponse
from apis.serializers import ProductSerializer
from apis.models import Product


def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(
        products,
        many=True,
    )

    return JsonResponse(
        {
            "data": serializer.data,
        }
    )
