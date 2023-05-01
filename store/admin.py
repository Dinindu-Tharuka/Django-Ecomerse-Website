from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count, Func,F, Value
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, Collection, Customer, Order
from urllib.parse import urlencode


class ProductPriceFilter(admin.SimpleListFilter):
    LESSTHAN_2000 = '<2000'
    LESSTHAN_4000 = '<4000'
    GREATERTHAN_4000 = '>4000'

    title = 'Price_Range'
    parameter_name = 'pricerange'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            (self.LESSTHAN_2000, 'Low'),
            (self.LESSTHAN_4000,'Middle'),
            (self.GREATERTHAN_4000, 'High')
        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == self.LESSTHAN_2000:
            return queryset.filter(unit_price__lte=2000)
        elif self.value() == self.LESSTHAN_4000:
            return queryset.filter(unit_price__lte=4000, unit_price__gt=2000)
        elif self.value() == self.GREATERTHAN_4000:
            return queryset.filter(unit_price__gt=4000)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_price']
    list_per_page = 10
    list_display = ['title', 'unit_price', 'price_range', 'collection']
    list_filter = ['collection', ProductPriceFilter]


    @admin.display(ordering='unit_price')
    def price_range(self, product):
        if product.unit_price > 2000:
            return 'High'
        else:
            return 'Low'
        
    @admin.action(description='Clear Price')
    def clear_price(self, request, queryset:QuerySet):
        no_of_product = queryset.update(unit_price=10)

        self.message_user(
            request,
            f'{no_of_product} products you have updated.'
        )

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
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['place_at', 'customer_name']
    list_select_related = ['customer']
    
    

    def customer_name(self, order):
        return order.customer_name
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            customer_name = Func(F('customer__first_name'), Value(' '), F('customer__last_name'), function='CONCAT')
        )
    
    


