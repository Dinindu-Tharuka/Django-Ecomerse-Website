from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection, OrderItem

######### Product ############

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 

    def destroy(self, request, *args, **kwargs):
        
        if OrderItem.objects.filter(product__id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)  

     
    
    
############## Collection End Point ###########

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('product')).all()
    serializer_class = CollectionSerializer 

    def destroy(self, request, *args, **kwargs):

        if Product.objects.filter(collection__id=kwargs['pk']).count() > 0:
            return Response({'error': "You can't delete this collection, because this collection has some products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    


    
    







    

