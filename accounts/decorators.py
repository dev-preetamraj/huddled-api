import logging
from functools import wraps
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql import GraphQLError
from graphene import ResolveInfo

from accounts.jwt_manager import JwtManager

User = get_user_model()

# Get an instance of logger
logger = logging.getLogger('accounts')


def get_email_from_auth_header(auth_header):
    access_token = auth_header[7:]
    jwt_manager = JwtManager()

    if not jwt_manager.verify_token(access_token):
        raise GraphQLError('Access token is invalid or expired')

    payload = jwt_manager.get_payload(access_token)
    email = payload.get('sub')
    return email


def update_last_login(user):
    user.last_login = timezone.localtime()
    user.save()


def is_admin_helper(info) -> None:
    user = info.context.user
    if not user.is_staff:
        raise GraphQLError('Admin access is required')


def login_helper(info) -> None:
    auth_header = info.context.headers.get('Authorization')
    if not auth_header:
        raise GraphQLError('Authorization header not provided')

    if not auth_header.startswith('Bearer '):
        raise GraphQLError('Invalid token type in header')

    email = get_email_from_auth_header(auth_header)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as ne:
        logger.error(f'decorator - login_helper : {ne}')
        raise GraphQLError('User not found')
    except Exception as e:
        logger.error(f'decorator - login_helper : {e}')
        raise GraphQLError('Invalid token')

    update_last_login(user)
    info.context.user = user


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = next(arg for arg in args if isinstance(arg, ResolveInfo))
        login_helper(info)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = next(arg for arg in args if isinstance(arg, ResolveInfo))
        is_admin_helper(info)
        return func(*args, **kwargs)

    return wrapper
