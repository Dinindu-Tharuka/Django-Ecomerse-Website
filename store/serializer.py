from decimal import Decimal
from rest_framework import serializers
from .models import Product

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_total_price')
    collection = CollectionSerializer()

    def calculate_total_price(self, product:Product):
        return round(product.unit_price * Decimal(1.1), 2)
    
class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=50)
    membership = serializers.CharField(max_length=1)