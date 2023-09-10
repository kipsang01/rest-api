from django.urls import path, include
from rest_framework import routers

from .views import CustomerViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
    ]