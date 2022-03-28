from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import  authenticate, login, logout
from rest_framework.decorators import action

from .models import User
from .serializers import *
from .services import *
from .permissions import *


'''
	jwt token based user login and logout
'''
class AuthenticationViewSet(viewsets.ViewSet):
    
    @action(detail = False, methods = ['post'], permission_classes = [permissions.AllowAny])
    def user_login(self, request):
        try:
            user = authenticate(request, email = request.data.get("email", ""), 
                    password = request.data.get("password", ""))

            if user is not None:
                login(request, user)
                payload = create_token(user)
                return Response(payload)

            return Response({
                'status': False, 
                'message': 'Invalid user credentials'}, 
                status = status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'status': False, 
                'message': str(e)}, 
                status = status.HTTP_400_BAD_REQUEST)


    @action(detail = False, methods = ['post'], permission_classes = [permissions.AllowAny])
    def user_logout(self, request):
        logout(request)
        return Response({
            'status': True,
            'message': 'User logged out successfully'}, 
            status = status.HTTP_200_OK)


'''
	Create, read, update and delete admin
	with backend filtering
'''
class AdminViewSet(viewsets.ModelViewSet):
    __basic_fields = ('name', 'mobile', 'email', 'location__name')
    
    queryset = User.objects.filter(is_admin = True).order_by('name')
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = __basic_fields
    permission_classes = (AdminPermission,)
    pagination_class = None	


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return super().get_serializer_class()


'''
	Induvidual Profile for admin and super admin
'''
class ProfileViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk = None):
        profile = request.user
        serializer = UserDetailSerializer(profile, context={"request": request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    def partial_update(self, request, pk = None):
        serializer = UserSerializer(request.user, data = request.data, partial = True, context={"request": request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)


'''

	Reset password
'''
class ChangePasswordViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
 
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordChangeSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        if not user.check_password(serializer.data.get("old_password")):
            return Response({
                'status': False,
                'old_password': 'Old password is incorrect'}, 
                status = status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.data.get("new_password"))
        user.save()
        
        return Response({
            'status': True,
            'message': 'Password updated successfully'}, 
            status = status.HTTP_200_OK)


