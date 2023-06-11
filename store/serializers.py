from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart, CartItem
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'product_count']

    product_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description',
                  'unit_price', 'collection', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, product):
        return product.unit_price * Decimal(2.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        print(validated_data)
        return Reviews.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']

    product = SimpleProductSerializer()

    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity


class SimpleCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "Product can'be found on this ID")
        else:
            return value

    def save(self, **kwargs):

        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']

        try:
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance


class CartItemUpdaterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = [ 'quantity']

    


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'cartitem', 'total']

    total = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, my_cart: Cart):
        return sum([x.quantity * x.product.unit_price for x in my_cart.cartitem.all()])

    cartitem = CartItemSerializer(many=True, read_only=True)
