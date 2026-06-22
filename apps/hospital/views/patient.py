from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminReceptionistOrReadOnly
from apps.hospital.models import Patient
from apps.hospital.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminReceptionistOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'phone', 'blood_group']