import graphene
from accounts.jwt_manager import JwtManager
from accounts.schema.types import AuthTokenType, RefreshTokenType
from django.contrib.auth import get_user_model
from graphql import GraphQLError


User = get_user_model()


class TokenMutation(graphene.Mutation):
    data = graphene.Field(AuthTokenType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        email: str,
        password: str,
    ):
        try:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                jwt_manager = JwtManager()
                access_token = jwt_manager.generate_access_token(email)
                refresh_token = jwt_manager.generate_refresh_token(email)
                data = {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
                return TokenMutation(data=data)
            else:
                raise GraphQLError('Given credentials are wrong')
        except Exception as e:
            print(e)
            raise GraphQLError('Something went wrong')


class RefreshTokenMutation(graphene.Mutation):
    data = graphene.Field(RefreshTokenType)

    class Arguments:
        refresh_token = graphene.String(required=True)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        refresh_token: str
    ):
        try:
            jwt_manager = JwtManager()
            access_token = jwt_manager.refresh_access_token(refresh_token)
            if access_token is not None:
                data = {
                    'access_token': access_token
                }
                return RefreshTokenMutation(data=data)
            else:
                raise GraphQLError('Refresh token is expired or invalid')
        except Exception as e:
            print(e)
            raise GraphQLError('Something went wrong')


class VerifyTokenMutation(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        access_token = graphene.String(required=True)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        access_token: str
    ):
        jwt_manager = JwtManager()
        if jwt_manager.verify_token(access_token):
            return VerifyTokenMutation(message='Access token verified')
        else:
            raise GraphQLError('Access token is expired or invalid')
