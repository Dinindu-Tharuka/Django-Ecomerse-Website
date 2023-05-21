from django.urls import path, include
from . import views
from rest_framework_nested.routers import NestedSimpleRouter, DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

product_neted_router = NestedSimpleRouter(router, 'products', lookup='product')
product_neted_router.register('review', views.ReviewViewSet, basename='product-reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_neted_router.urls)),
    
    
]
