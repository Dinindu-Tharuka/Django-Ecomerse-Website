from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product, OrderItem, Order

def say_hello(request):

    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set')\
                .order_by('place_at')[:5]
    

    count = query_set.count()
    


    return render(request, 'hello.html', {'products' : list(query_set), 'count':count})
