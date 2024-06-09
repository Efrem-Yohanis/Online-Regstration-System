from rest_framework import serializers
from app1.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }