from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from store.models import Product

def say_hello(request):

    product = Product.objects.filter(Q(unit_price__gt=3000) | Q(unit_price__lt=4000))
    count_product = product.count()

    return render(request, 'hello.html', {'products' : list(product), 'count':count_product})
