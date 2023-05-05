from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import Response

@api_view()
def product_list(request):
    return Response('Ok')

@api_view()
def product_details(request, id):
    return Response(id)