from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType

from friendship.models import Friendship

User = get_user_model()


class FriendshipNode(DjangoObjectType):
    class Meta:
        model = Friendship
        interfaces = (relay.Node,)
