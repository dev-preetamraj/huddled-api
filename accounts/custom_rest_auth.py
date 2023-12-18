import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response

# Get an instance of logger
logger = logging.getLogger('accounts')

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        user_id = authorization_header.split(' ')[1]

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(detail='User not found. Invalid credentials')

        return user, None
