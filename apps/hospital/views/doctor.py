from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsAdminReceptionistOrReadOnly
from apps.hospital.models import Doctor
from apps.hospital.serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user', 'department').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminReceptionistOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'specialization', 'department__name']
    ordering_fields = ['experience','specialization']
    ordering = ['id']

    @action(detail=False, methods=['get'])
    def available(self, request):
        doctors = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)
    
    

