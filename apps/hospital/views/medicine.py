from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminReceptionistOrReadOnly
from apps.hospital.models import Medicine
from apps.hospital.serializers import MedicineSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminReceptionistOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'unit']