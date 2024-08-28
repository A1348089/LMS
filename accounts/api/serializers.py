from rest_framework import serializers

from accounts.models import CustomUser

class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'is_mentor','is_intern']
