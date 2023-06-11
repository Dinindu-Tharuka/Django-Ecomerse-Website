from django_filters.rest_framework import FilterSet
from .models import Product

class ProductPriceFilter(FilterSet):
    class Meta:
        model=Product
        fields={
            'collection_id':['exact'],
            'unit_price':['gt', 'lt']
        }