from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from datetime import date
from rest_framework.decorators import action

from account.models import User
from location.models import Location
from shop.models import Service, Category
from advertisement.models import Advertisement
from .serializers import *


class HomeView(viewsets.ViewSet):
	permission_classes = (permissions.AllowAny,)
	pagination_class = None

	def list(self, request):
		data = self.get_objects()
		serializer = HomeSerializer(data, context={"request": request})
		return Response(serializer.data, status = status.HTTP_200_OK)

	def get_objects(self):
		recent_locations = Location.objects.all().order_by('-id')[:10]
		#recent_services = Service.objects.all().order_by('-id')[:8]

		today = date.today()
		ads = Advertisement.objects.filter(location = None, expiry__gte = today, ad_type = 'small')
		large_ads = Advertisement.objects.filter(expiry__gte = today, ad_type = 'large')

		return {
			'recent_locations': recent_locations,
			'ads': ads,
			'large_ads': large_ads
		}


class ServiceSggestionView(viewsets.ViewSet):
	permission_classes = (permissions.AllowAny,)
	pagination_class = None


	@action(detail = False, methods = ['get'], permission_classes = [permissions.AllowAny])
	def recommendations(self, request):
		name = self.request.GET.get('name', None)
		location = self.request.GET.get('location', None)
		categories = Category.objects.filter(name__icontains = name)[:5]
		services = Service.objects.filter(admin__location__name = location, name__icontains = name)[:5]

		obj = {
			'services': services,
			'categories': categories
		}

		serializer = ServiceFilterSerializer(obj)
		return Response(serializer.data, status = status.HTTP_200_OK)
