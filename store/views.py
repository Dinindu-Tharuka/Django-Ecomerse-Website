from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
 
@api_view()
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True, context={'request':request})
    return Response(serializer.data)

@api_view()
def product_item(request, id):
    product = Product.objects.get(pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collection_list(request):
    collection = Collection.objects.all()
    serializer = CollectionSerializer(collection, many=True)
    return Response(serializer.data)

@api_view()
def collection_item(request, id):
    return Response('Ok')