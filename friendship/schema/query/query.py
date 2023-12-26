import logging

import graphene
from graphene import relay
from graphql import GraphQLError

from accounts.decorators import login_required
from accounts.schema.types import UserConnection
from friendship.models import Friendship

# Get an instance of logger
logger = logging.getLogger("friendship")


class FriendshipQuery(graphene.ObjectType):
    friend_requests = relay.ConnectionField(UserConnection)
    sent_requests = relay.ConnectionField(UserConnection)

    @login_required
    def resolve_friend_requests(self, info, **kwargs):
        try:
            user = info.context.user
            friendships = Friendship.objects.filter(
                friend=user, is_accepted=False
            ).all()
            requests = [friendship.user for friendship in friendships]
            return requests
        except Exception as e:
            logger.error(f'FriendshipQuery -> resolve_friend_requests: {e}')
            raise GraphQLError("Something went wrong")

    @login_required
    def resolve_sent_requests(self, info, **kwargs):
        try:
            user = info.context.user
            friendships = Friendship.objects.filter(
                user=user, is_accepted=False).all()
            sent_requests = [friendship.friend for friendship in friendships]
            return sent_requests
        except Exception as e:
            logger.error(f'FriendshipQuery -> resolve_sent_requests: {e}')
            raise GraphQLError("Something went wrong")
