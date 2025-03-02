from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'number', 'is_active', 'is_staff', 'data_joined']
        read_only_fields = ['id', 'is_active', 'is_staff', 'data_joined']
