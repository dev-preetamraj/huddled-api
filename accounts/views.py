import logging
import cloudinary.uploader
from rest_framework import status
from rest_framework.decorators import api_view
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
                email=email,
                username=email,
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
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


@api_view(['post'])
def update_user_picture(request, slug):
    try:
        user = request.user
        picture = request.data.get('picture')
        url = ''
        try:
            if slug not in ['cover', 'profile']:
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Slug must be one of the following: [cover, profile]',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            res = cloudinary.uploader.upload(
                picture,
                public_id=f'{user.email.replace(".", "_").replace("@", "_")}_{slug}_picture',
                overwrite=True,
                folder=f'huddled/images/{user.email}',
                face=True
            )
            url = res.get('secure_url')

            if slug == 'cover':
                user.cover_picture = url
            elif slug == 'profile':
                user.profile_picture = url

            user.save()
        except Exception as e:
            logger.error(e)

        return Response({
            'success': True,
            'status_code': status.HTTP_201_CREATED,
            'message': 'Cover photo updated successfully',
            'data': url
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f'update_profile_picture | Error: {e}')
        return Response({
            'success': False,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Something went wrong',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
