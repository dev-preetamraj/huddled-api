import logging

import graphene
from django.contrib.auth import get_user_model
from graphene import relay

from accounts.decorators import login_required, admin_required
from accounts.schema.types import UserNode, UserConnection

User = get_user_model()

# Get an instance of logger
logger = logging.getLogger("accounts")


class AccountsQuery(graphene.ObjectType):
    get_users = relay.ConnectionField(UserConnection)
    me = graphene.Field(UserNode)
    suggested_users = relay.ConnectionField(UserConnection)
    user_by_id = graphene.Field(UserNode, user_id=graphene.String(required=True))

    @admin_required
    @login_required
    def resolve_get_users(self, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_suggested_users(self, info):
        requested_user = info.context.user
        users = User.objects.exclude(id=requested_user.id)
        data = []

        for user in users:
            friendship = requested_user.friends.filter(friend=user).first()
            if friendship is None:
                data.append(user)
        return data

    @login_required
    def resolve_user_by_id(self, info, user_id: str):
        user = User.objects.get(id=user_id)
        return user
