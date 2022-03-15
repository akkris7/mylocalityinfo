from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User
from location.serializers import LocationSerializer


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(
	    write_only = True,
	    style = {'input_type': 'password', 'placeholder': 'Password'}
	)

	class Meta:
		model = User
		fields = ('id', 'name', 'mobile', 'email', 
			      'profile_pic', 'created_at', 'location', 
			      'password', 'is_admin')


	def to_representation(self, instance):
		rep = super(UserSerializer, self).to_representation(instance)
		try:
			rep['location'] = instance.location.name
		except:
			rep['location'] = ''
		return rep


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance:
			self.fields.pop('password')


	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data.get('password'))
		return super(UserSerializer, self).create(validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
	location = LocationSerializer(read_only = True)

	class Meta:
		model = User
		fields = ('id', 'name', 'mobile', 'email', 
			      'profile_pic', 'created_at', 'location', 
			      'is_admin', 'updated_at', 'last_login')


class PasswordChangeSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(write_only = True)
	password = serializers.CharField(
	    write_only = True,
	    style = {'input_type': 'password', 'placeholder': 'Password'}
	)	