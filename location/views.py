from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import *
from .serializers import *
from .permissions import *


class LocationViewSet(viewsets.ModelViewSet):
	__basic_fields = ('name',)
	queryset = Location.objects.all().order_by('name')
	serializer_class = LocationSerializer
	filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
	search_fields = __basic_fields
	permission_classes = (LocationPermission,)
	pagination_class = None