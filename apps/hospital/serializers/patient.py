from rest_framework import serializers

from apps.hospital.models import Patient
from .user import UserSerializer


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

    def validate_user(self, value):
        request = self.context.get('request')
        if (
            request
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'patient'
            and value != request.user
        ):
            raise serializers.ValidationError(
                'You can only create or update your own patient profile.'
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if (
            request
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'patient'
        ):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if (
            request
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'patient'
        ):
            validated_data.pop('user', None)
        return super().update(instance, validated_data)