from rest_framework import serializers

from apps.hospital.models import Appointment, Prescription, PrescriptionMedicine
from .medicine import MedicineSerializer


class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    medicine_detail = MedicineSerializer(source='medicine', read_only=True)

    class Meta:
        model = PrescriptionMedicine
        fields = [
            'id',
            'medicine',
            'medicine_detail',
            'dosage',
            'duration',
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'appointment',
            'diagnosis',
            'notes',
            'created_at',
            'medicines',
        ]
        read_only_fields = ['created_at']

    def validate_appointment(self, value):
        if value.status != Appointment.Status.COMPLETED:
            raise serializers.ValidationError(
                'Prescription can only be created for completed appointments.'
            )

        if hasattr(value, 'prescription'):
            raise serializers.ValidationError(
                'Prescription already exists for this appointment.'
            )

        return value

    def validate_medicines(self, value):
        if not value:
            raise serializers.ValidationError(
                'At least one medicine is required.'
            )
        return value

    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines')
        prescription = Prescription.objects.create(**validated_data)

        for medicine_data in medicines_data:
            PrescriptionMedicine.objects.create(
                prescription=prescription,
                **medicine_data
            )

        return prescription