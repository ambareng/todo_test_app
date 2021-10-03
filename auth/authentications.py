import jwt
import json

from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication


class JWTAuthentication(BaseAuthentication):
    model = User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = User
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user_id = payload['id']
        msg = {'Error': "Token mismatch", 'status': "401"}
        try:
            user = User.objects.get(id=user_id)
            # if not user.token['token'] == token:
            #     raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError or jwt.DecodeError or jwt.InvalidTokenError:
            return Response({'Error': "Token is invalid"}, status="403")
        except User.DoesNotExist:
            return Response({'Error': "Internal server error"}, status="500")

        return user, token

    def authenticate_header(self, request):
        return 'Token'

    @staticmethod
    def get_current_user(request):
        auth = get_authorization_header(request).split()
        token = auth[1]
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        user_id = payload['id']
        user = User.objects.get(id=user_id)
        return user
