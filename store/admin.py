from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, Collection, Customer, Order
from urllib.parse import urlencode

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['title', 'unit_price', 'price_range', 'collection']


    @admin.display(ordering='unit_price')
    def price_range(self, product):
        if product.unit_price > 2000:
            return 'High'
        else:
            return 'Low'

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['title', 'product_count']

    def product_count(self, collection):

       

        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id':collection.id
               })
               )


        return format_html('<a href="{}">{}</a>', url, collection.product_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['place_at', 'customer', 'customer_last_name']
    list_select_related = ['customer']
    

    def customer(self, order):
        return order.customer
    
    def customer_last_name(self, order):
        return order.customer.last_name


