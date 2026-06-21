from rest_framework import serializers
from .models import (
    User,
    Doctor,
    Patient,
    Department,
    Appointment,
    Prescription,
    PrescriptionMedicine,
    Medicine,
    Bill,
)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'date_joined',
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'user',
            'user_detail',
            'department',
            'department_detail',
            'specialization',
            'phone',
            'experience',
            'is_available',
        ]


class PatientSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'user_detail',
            'age',
            'gender',
            'blood_group',
            'address',
            'phone',
        ]


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

    def validate_status(self, value):
        allowed_statuses = ['pending', 'approved', 'completed', 'cancelled']

        if value not in allowed_statuses:
            raise serializers.ValidationError('Invalid appointment status.')

        return value


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    medicine_detail = MedicineSerializer(source='medicine', read_only=True)

    class Meta:
        model = PrescriptionMedicine
        fields = [
            'id',
            'prescription',
            'medicine',
            'medicine_detail',
            'dosage',
            'duration',
        ]
        read_only_fields = ['prescription']


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

    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines')
        prescription = Prescription.objects.create(**validated_data)

        for medicine_data in medicines_data:
            PrescriptionMedicine.objects.create(
                prescription=prescription,
                **medicine_data
            )

        return prescription


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