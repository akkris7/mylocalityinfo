from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('accounts/', include('account.urls')),
    path('services/', include('shop.urls')),
    path('ads/', include('advertisement.urls')),
    path('location/', include('location.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('home/', include('home.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
