from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)


urlpatterns = router.urls
# [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetails.as_view()),
#     path('collection/', views.CollectionList.as_view()),
#     path('collection/<int:pk>/', views.CollectionDetails.as_view())
# ]