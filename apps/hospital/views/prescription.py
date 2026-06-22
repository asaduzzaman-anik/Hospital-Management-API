from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.hospital.models import Prescription
from apps.hospital.serializers import PrescriptionSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related(
        'appointment',
        'appointment__patient',
        'appointment__patient__user',
        'appointment__doctor',
        'appointment__doctor__user',
    ).prefetch_related('medicines', 'medicines__medicine').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.role == 'doctor':
            return queryset.filter(appointment__doctor__user=user)

        if user.role == 'patient':
            return queryset.filter(appointment__patient__user=user)

        return queryset