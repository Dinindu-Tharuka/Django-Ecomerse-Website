from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer
from .models import Product, Collection, OrderItem, Reviews, Cart, CartItem
from .filters import ProductPriceFilter
from .pagination import DefaultPagination


######### Product ############

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductPriceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = Product.objects.filter(collection_id=collection_id).all()
    #     return queryset

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
    

class ReviewViewSet(ModelViewSet):
    
    serializer_class = ReviewSerializer    
    
    def get_queryset(self):
        return Reviews.objects.filter(product__id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {
            'product_id':self.kwargs['product_pk']
        }
    
class CartViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer







    

    


    
    







    

