from rest_framework import viewsets

from apps.common.permissions import IsAdminOrReadOnly
from apps.hospital.models import Department
from apps.hospital.serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]