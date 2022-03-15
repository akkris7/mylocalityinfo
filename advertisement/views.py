from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from datetime import date

from .models import *
from .serializers import *
from payankor_api.pagination import CustomPagination

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all().order_by('id')
    serializer_class = AdvertisementSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('location__name',)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdvertisementDetailSerializer
        return super().get_serializer_class()


    @action(detail = False, methods = ['get'], permission_classes = [permissions.AllowAny])
    def local_ads(self, request):
        today = date.today()
        location_id = self.request.GET.get('location_id', None)
        queryset = self.queryset.filter(location = location_id, expiry__gte = today)
        serializer = AdvertisementMiniSerializer(queryset, context={"request": request}, many = True)
        return Response(serializer.data)