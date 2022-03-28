from rest_framework import serializers

from .models import Advertisement
from location.serializers import LocationSerializer
from location.models import Location


class AdvertisementSerializer(serializers.ModelSerializer):
	location = serializers.PrimaryKeyRelatedField(
		queryset = Location.objects.all(),
		required = False,
		allow_null = True
		)

	class Meta:
		model = Advertisement
		fields = ('__all__')


	def to_representation(self, instance):
		rep = super(AdvertisementSerializer, self).to_representation(instance)
		try:
			rep['location'] = instance.location.name
		except:
			rep['location'] = 'common'
		return rep


class AdvertisementDetailSerializer(serializers.ModelSerializer):
	location = LocationSerializer(read_only = True)
	
	class Meta:
		model = Advertisement
		fields = ('__all__')


class AdvertisementMiniSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField()

	class Meta:
		model = Advertisement
		fields = ('id', 'image')

	def get_image(self, obj):
		try:
			request = self.context.get('request')
			image = obj.image.url
			return request.build_absolute_uri(image)
		except:
			return None