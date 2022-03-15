from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'service-filter', views.ServiceSggestionView, basename = "home")
router.register(r'', views.HomeView, basename = "home")

urlpatterns = [
    path('', include(router.urls))
]