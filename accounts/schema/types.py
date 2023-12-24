import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType

from friendship.schema.types import FriendshipNode

User = get_user_model()


class UserNode(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = User
        exclude = ["password"]
        interfaces = (relay.Node,)


class UserConnection(relay.Connection):
    class Meta:
        node = UserNode


class DiscoverUserTypes(graphene.ObjectType):
    user = graphene.Field(UserNode)
    friendship = graphene.Field(FriendshipNode)


class DiscoverUserConnection(relay.Connection):
    class Meta:
        node = UserNode
