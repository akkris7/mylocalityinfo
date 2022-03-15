from rest_framework import viewsets, permissions, status
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import *
from payankor_api.pagination import CustomPagination
from payankor_api.large_pagination import LargePagination

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
	search_fields = ('name',)
	permission_classes = (permissions.IsAuthenticated,)
	pagination_class = None	


class ServiceViewSet(viewsets.ModelViewSet):
	__basic_fields = ('name', 'category__name', 'landmark', 'admin__name', 'admin__location__name')
	queryset = Service.objects.all().order_by('id')
	serializer_class = ServiceSerializer
	filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
	search_fields = __basic_fields
	permission_classes = (ServicePermission,)
	pagination_class = CustomPagination


	def get_serializer_class(self):
		if self.action == 'retrieve':
			return ServiceDetailSerializer
		return super().get_serializer_class()


	def get_queryset(self):
		if self.request.user.is_superuser:
			return self.queryset
		else:
			return self.queryset.filter(admin = self.request.user)


class ServiceFilteredViewSet(viewsets.ModelViewSet):
	queryset = Service.objects.all()
	serializer_class = ServiceListSerializer
	permission_classes = (permissions.AllowAny,)
	pagination_class = LargePagination


	def list(self, request):
		name = self.request.GET.get('name', None)
		location = self.request.GET.get('location', None)
		is_category = self.request.GET.get('is_category', None)

		if is_category == "yes":
			filtered_list = self.queryset.filter(admin__location__name = location, 
				category__name__icontains = name)

		else:
			filtered_list = self.queryset.filter(admin__location__name = location,
				name__icontains = name)

		serializer = ServiceListSerializer(filtered_list, context={"request": request},  many = True)
		page = self.paginate_queryset(serializer.data)
		return self.get_paginated_response(page)