from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection

######### Product ############

class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetails(APIView):   
    
    def get(self, request, id):     
        product = get_object_or_404(Product, pk=id)          
        seralizer = ProductSerializer(product)
        return Response(seralizer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
############## Collection End Point ###########

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('product')).all()
    serializer_class = CollectionSerializer 

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CollectionDetails(APIView):

    def get(self, request, id):
        queryset = Collection.objects.annotate(product_count=Count('product')).all()    
        collection = get_object_or_404(queryset, pk=id)
        serializer = CollectionSerializer(collection)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        collection = Collection.objects.get(pk=id)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, id):
        collection = Collection.objects.get(pk=id)
        if collection.product_set.count() > 0:
            return Response({'error': "You can't delete this collection, because this collection has some products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






    

