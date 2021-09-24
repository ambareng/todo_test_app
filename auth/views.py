from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView

from auth.serializers import UserSerializer


class Register(CreateAPIView):
    queryset = User
    serializer_class = UserSerializer
