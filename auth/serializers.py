from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        write_only_fields = ['password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            username=validated_data['username'],
        )
        user.save()
        return user
