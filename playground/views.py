from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product, OrderItem

def say_hello(request):

    orderitem_set = OrderItem.objects.values('product__title').distinct().order_by('product__title')

    # query_set = OrderItem.objects.values('product_id').distinct()

    # query_set_product = Product.objects.filter(id__in=query_set)
    
    count_product = orderitem_set.count()


    return render(request, 'hello.html', {'products' : list(orderitem_set), 'count':count_product})
