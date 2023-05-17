from django.urls import path
from . import views
from rest_framework_nested.routers import NestedSimpleRouter, DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

product_neted_router = NestedSimpleRouter(router, 'products', lookup='product')
product_neted_router.register('review', views.ReviewViewSet, basename='product-reviews')



urlpatterns = router.urls + product_neted_router.urls
# [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetails.as_view()),
#     path('collection/', views.CollectionList.as_view()),
#     path('collection/<int:pk>/', views.CollectionDetails.as_view())
# ]