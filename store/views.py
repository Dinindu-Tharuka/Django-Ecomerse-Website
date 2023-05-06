from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import Response
from rest_framework import status
from .serializer import ProductSerializer, CollectionSerializer, CustomerSerializer
from .models import Product, Collection, Customer

@api_view()
def product_list(request):
    product_queryset = Product.objects.select_related('collection').all()
    product_serializer = ProductSerializer(product_queryset, many=True)
    return Response(product_serializer.data)

@api_view()
def product_details(request, id):
    try:
        product = Product.objects.get(pk=id)
        product_serializer = ProductSerializer(product)
    except product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(product_serializer.data)


@api_view()
def collection_list(request):
    collection_queryset = Collection.objects.all()
    collection_serializer = CollectionSerializer(collection_queryset, many=True)

    return Response(collection_serializer.data)

@api_view()
def collection_details(request,id):
    try:
        collection = Collection.objects.get(pk=id)
        collection_serializer = CollectionSerializer(collection)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(collection_serializer.data)

@api_view()
def customers_list(request):
    customers = Customer.objects.all()
    customer_serializer = CustomerSerializer(customers)
    return Response(customer_serializer.data)


