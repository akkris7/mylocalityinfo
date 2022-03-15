from rest_framework import serializers

from .models import *
from account.serializers import UserDetailSerializer


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ('__all__')


class ServiceSerializer(serializers.ModelSerializer):

	location = serializers.SerializerMethodField('admin_location')

	def admin_location(self, obj):
		try:
			return obj.admin.location.name
		except:
			return "admin not assigned"

	class Meta:
		model = Service
		fields = ('id', 'name', 'contact', 'address', 'landmark', 'image',
				  'category', 'admin', 'location')

	def to_representation(self, instance):
		rep = super(ServiceSerializer, self).to_representation(instance)
		try:
			rep['category'] = instance.category.name
		except:
			rep['category'] = None
		try:
			rep['admin'] = instance.admin.name
		except:
			rep['admin'] = None
		return rep


class ServiceDetailSerializer(serializers.ModelSerializer):
	admin = UserDetailSerializer(read_only = True)
	category = CategorySerializer(read_only = True)
	
	class Meta:
		model = Service
		fields = ('__all__')


class ServiceMiniSerializer(serializers.ModelSerializer):

	class Meta:
		model = Service
		fields = ('id', 'name')


class ServiceListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Service
		fields = ('id', 'name', 'image', 'address', 'contact')


	def get_image(self, obj):
		try:
			request = self.context.get('request')
			image = obj.image.url
			return request.build_absolute_uri(image)
		except:
			return None