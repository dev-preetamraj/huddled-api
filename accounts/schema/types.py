import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ['password']


class AuthTokenType(graphene.ObjectType):
    access_token = graphene.String()
    refresh_token = graphene.String()


class RefreshTokenType(graphene.ObjectType):
    access_token = graphene.String()
