from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet, basename = "category")
router.register(r'filtered_services', views.ServiceFilteredViewSet, basename = "filtered")
router.register(r'', views.ServiceViewSet, basename = "service")

urlpatterns = [
    path('', include(router.urls))
]