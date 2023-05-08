from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    class Meta:
        model = Collection
        fiels = ['id', 'title']
    


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax_price')
    # collection = serializers.HyperlinkedRelatedField(queryset = Collection.objects.all(), view_name='collection-item')

    def calculate_tax_price(self, product:Product):
        return round(product.unit_price * Decimal(1.1),2)

    
