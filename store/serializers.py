from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart,CartItem
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'product_count']

    product_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'collection', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='total')
    
    def total(self, product):
        return product.unit_price * Decimal(2.1)




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reviews
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id=product_id, **validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'title', 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id', 'quantity', 'product', 'total_price']

    product = SimpleProductSerializer()

    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.unit_price * cart_item.quantity   
   
    
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model= Cart
        fields=['id', 'cartitem', 'total']
    
    total = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, my_cart:Cart):
        return sum([x.quantity * x.product.unit_price for x in my_cart.cartitem.all()])

    cartitem = CartItemSerializer(many=True)
        



