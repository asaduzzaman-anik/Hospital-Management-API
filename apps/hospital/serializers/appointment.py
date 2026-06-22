from django.utils import timezone
from rest_framework import serializers

from apps.hospital.models import Appointment
from .doctor import DoctorSerializer
from .patient import PatientSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'patient_detail',
            'doctor',
            'doctor_detail',
            'appointment_date',
            'status',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Appointment date cannot be in the past.'
            )
        return value

    def validate(self, attrs):
        doctor = attrs.get('doctor')

        if doctor and not doctor.is_available:
            raise serializers.ValidationError(
                {'doctor': 'Selected doctor is not available.'}
            )

        return attrs