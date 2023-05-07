from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>', views.product_item),
    path('collection/<int:pk>', views.collection_item, name='collection-item'),
    path('collection/', views.collection_list)
]
