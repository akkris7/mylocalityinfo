from rest_framework import serializers

from shop.serializers import ServiceListSerializer, ServiceMiniSerializer, CategorySerializer
from location.serializers import LocationSerializer
from advertisement.serializers import AdvertisementSerializer


class HomeSerializer(serializers.Serializer):
	recent_services = ServiceListSerializer(many = True)
	recent_locations = LocationSerializer(many = True)
	ads = AdvertisementSerializer(many = True)


class ServiceFilterSerializer(serializers.Serializer):
	services = ServiceMiniSerializer(many = True)
	categories = CategorySerializer(many = True)