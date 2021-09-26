import jwt
import datetime

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from auth.serializers import UserSerializer


class Register(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = User
    serializer_class = UserSerializer


class Login(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        user = get_object_or_404(User, email=request.data['email'])
        if check_password(request.data['password'], user.password):
            key = 'secret'
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            encoded = jwt.encode(payload, key, algorithm='HS256')
            return Response({
                'jwt': f'Token {encoded}'
            })
        return Response({
            'error': 'Invalid email or password'
        })
