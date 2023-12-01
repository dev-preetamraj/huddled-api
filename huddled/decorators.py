from functools import wraps
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from graphene import ResolveInfo

from accounts.jwt_manager import JwtManager

User = get_user_model()


def get_email_from_auth_header(auth_header):
    if not auth_header:
        raise GraphQLError('Authorization header not provided')

    if not auth_header.startswith('Bearer '):
        raise GraphQLError('Invalid token type in header')

    access_token = auth_header[7:]
    jwt_manager = JwtManager()

    if not jwt_manager.verify_token(access_token):
        raise GraphQLError('Access token is invalid or expired')

    payload = jwt_manager.get_payload(access_token)
    email = payload.get('sub')
    return email


def is_admin_helper(info) -> None:
    user = info.context.user
    if not user.is_staff:
        raise GraphQLError('Admin access is required')


def login_helper(info) -> None:
    auth_header = info.context.headers.get('Authorization')
    email = get_email_from_auth_header(auth_header)

    try:
        user = User.objects.get(email=email)
        info.context.user = user

    except Exception as e:
        print(e)
        raise GraphQLError('Invalid token')


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
