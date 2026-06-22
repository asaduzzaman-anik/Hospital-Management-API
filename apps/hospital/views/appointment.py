from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hospital.models import Appointment
from apps.hospital.serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related(
        'patient',
        'patient__user',
        'doctor',
        'doctor__user',
        'doctor__department',
    ).all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'patient', 'appointment_date', 'status']
    ordering_fields = ['appointment_date','created_at']
    ordering = ['-appointment_date']
    
    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.role == 'doctor':
            return queryset.filter(doctor__user=user)

        if user.role == 'patient':
            return queryset.filter(patient__user=user)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'patient':
            serializer.save(patient=user.patient)
        else:
            serializer.save()

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
        return Response(self.get_serializer(appointment).data)

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = Appointment.Status.APPROVED
        appointment.save()
        return Response(self.get_serializer(appointment).data)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        return Response(self.get_serializer(appointment).data)
    