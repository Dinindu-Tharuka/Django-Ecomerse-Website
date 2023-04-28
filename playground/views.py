from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models import Max
from store.models import Product, OrderItem, Order, Customer
from django.contrib.contenttypes.models import ContentType
from tag.models import TagItem


def say_hello(request):

    content_model = ContentType.objects.get_for_model(Product)

    query_set = TagItem.objects.select_related('tag').filter(
        content_type = content_model,
        object_id = 3
    )
    

    # count = query_set.count()
    return render(request, 'hello.html', {'products' : query_set})
