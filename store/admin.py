from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.db.models import Count, Func,F, Value
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, Collection, Customer, Order, OrderItem, Promotion
from tag.models import TagItem
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
        
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TagItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ###### Forms
    prepopulated_fields = {
        'slug':['title']
    }
    autocomplete_fields = ['collection']
    inlines = [TagInline]

    actions = ['clear_price']
    list_per_page = 10
    list_display = ['title', 'unit_price', 'price_range', 'collection']
    list_filter = ['collection', ProductPriceFilter]
    search_fields = ['title']

    


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

class ProductInline(admin.StackedInline):
    model=Product
    extra = 0

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['title', 'product_count']
    search_fields = ['title']
    inlines = [ProductInline]

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
    list_display = ['customer_name', 'membership']
    list_editable = ['membership']
    list_filter = ['membership']    
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def customer_name(self, customer):
        return customer.full_name
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
        )


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    autocomplete_fields = ['product']
    extra = 0




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_per_page = 10
    list_display = [ 'customer_name', 'products', 'place_at' ]
    list_select_related = ['customer']
    inlines= [OrderItemInline]
    
    @admin.display(ordering='products')
    def products(self, order):    

        url = (reverse('admin:store_orderitem_changelist')
               + '?'
               + urlencode({
                   'order__id':order.id
               }))   

        return format_html('<a href="{}">{}</a>', url, order.products )    
    

    def customer_name(self, order):
        return order.customer_name
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            customer_name = Func(F('customer__first_name'), Value(' '), F('customer__last_name'), function='CONCAT'),
            products= Count('orderitem')
        )
    
class OrderItemFilter(admin.SimpleListFilter):
    title = 'Item_Range'
    parameter_name = 'itemrange'

    LOW = '<300'
    MIDDLE = '<500'
    HIGH = '>500'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            (self.LOW, 'Low'),
            (self.MIDDLE, 'Middle'),
            (self.HIGH, 'High')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == self.LOW:
            return queryset.filter(quantity__lte=300)
        elif self.value() == self.MIDDLE:
            return queryset.filter(quantity__lte=500, quantity__gt=300)
        elif self.value() == self.HIGH:
            return queryset.filter(quantity__gt=500)

    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'quantity']
    list_filter = [OrderItemFilter]
    list_per_page = 15

    def products(self, orderitem):
        return orderitem.products
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products=Count('product')
        )
    
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    search_fields = ['description']
    
    


