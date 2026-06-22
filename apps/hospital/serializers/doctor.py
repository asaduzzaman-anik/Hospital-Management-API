from rest_framework import serializers

from apps.hospital.models import Doctor
from .department import DepartmentSerializer
from .user import UserSerializer


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