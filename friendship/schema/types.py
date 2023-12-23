from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from friendship.models import Friendship

User = get_user_model()


class FriendshipType(DjangoObjectType):
    class Meta:
        model = Friendship
