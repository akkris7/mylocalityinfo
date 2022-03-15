from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = routers.DefaultRouter()
router.register(r'admins', views.AdminViewSet, basename = "admins")
router.register(r'profile', views.ProfileViewSet, basename = "profile")
router.register(r'change-password', views.ChangePasswordViewSet, basename = "change password")
router.register(r'', views.AuthenticationViewSet, basename = 'auth')

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('', include(router.urls))
]