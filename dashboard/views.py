from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from account.models import User
from location.models import Location
from shop.models import Service, Category

class DashboardView(viewsets.ViewSet):
	permission_classes=(permissions.IsAuthenticated,)
	
	def list(self, request):
		total_admins = User.objects.filter(is_admin = True).count()
		total_locations = Location.objects.all().count()
		total_shops = Service.objects.all().count()
		total_categories = Category.objects.all().count()

		return Response({
			'total_admins': total_admins,
			'total_locations': total_locations,
			'total_shops': total_shops,
			'total_categories': total_categories
		})