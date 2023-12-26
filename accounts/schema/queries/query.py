import logging

import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphql import GraphQLError

from accounts.decorators import login_required, admin_required
from accounts.schema.types import UserNode, UserConnection
from friendship.models import Friendship

User = get_user_model()

# Get an instance of logger
logger = logging.getLogger("accounts")


class AccountsQuery(graphene.ObjectType):
    get_users = relay.ConnectionField(UserConnection)
    me = graphene.Field(UserNode)
    suggested_users = relay.ConnectionField(UserConnection)
    user_by_id = graphene.Field(
        UserNode, user_id=graphene.String(required=True))

    @login_required
    @admin_required
    def resolve_get_users(self, info, **kwargs):
        try:
            return User.objects.all()
        except Exception as e:
            logger.error(f'AccountsQuery -> resolve_get_users: {e}')
            raise GraphQLError("Something went wrong")

    @login_required
    def resolve_me(self, info):
        try:
            return info.context.user
        except Exception as e:
            logger.error(f'AccountsQuery -> resolve_me: {e}')
            raise GraphQLError("Something went wrong")

    @login_required
    def resolve_suggested_users(self, info, **kwargs):
        try:
            requested_user = info.context.user
            users = User.objects.exclude(id=requested_user.id)
            data = []

            for user in users:
                friendship = (
                    Friendship.objects.filter(
                        user=user, is_accepted=False).first()
                    or Friendship.objects.filter(friend=user, is_accepted=False).first()
                )
                if friendship is None:
                    data.append(user)
            return data
        except Exception as e:
            logger.error(f'AccountsQuery -> resolve_suggested_users: {e}')
            raise GraphQLError("Something went wrong")

    @login_required
    def resolve_user_by_id(self, info, user_id: str):
        try:
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            logger.error(f'AccountsQuery -> resolve_user_by_id: {e}')
            raise GraphQLError("Something went wrong")
