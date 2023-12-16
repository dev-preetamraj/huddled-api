import logging
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

logger = logging.getLogger('accounts')

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data.get('data')
            user_id = data.get('id')
            email = ''
            primary_email_id = data.get('primary_email_address_id')
            for email_address in data['email_addresses']:
                if email_address.get('id') == primary_email_id:
                    email = email_address.get('email_address')
                    break

            user = User(
                id=user_id,
                email=email
            )
            user.save()
            return Response({
                'success': True,
                'status_code': status.HTTP_201_CREATED,
                'message': 'User created successfully',
                'data': None
            })
        except Exception as e:
            logger.error(f'RegisterView error: {e}')
            return Response({
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Something went wrong',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
