from rest_framework import serializers

from apps.hospital.models import Bill
from .patient import PatientSerializer


class BillSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id',
            'patient',
            'patient_detail',
            'amount',
            'paid',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Bill amount must be greater than zero.'
            )
        return value