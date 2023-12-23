import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from friendship.models import Friendship
from friendship.schema.types import FriendshipType

User = get_user_model()


class UserType(DjangoObjectType):

    class Meta:
        model = User
        exclude = ['password']


class DiscoverUserTypes(graphene.ObjectType):
    user = graphene.Field(UserType)
    friendship = graphene.Field(FriendshipType)
