import logging

import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from accounts.decorators import login_required
from friendship.models import Friendship

User = get_user_model()

logger = logging.getLogger("friendship")


class AddFriendMutation(graphene.Mutation):
    class Arguments:
        friend_id = graphene.String(required=True)

    message = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, friend_id: str):
        try:
            user = info.context.user
            friend = User.objects.get(id=friend_id)
            Friendship.objects.create(user=user, friend=friend)
            return AddFriendMutation(message="Friend request sent successfully")
        except Exception as e:
            logger.error(f"AddFriendMutation error: {e}")
            raise GraphQLError("Something went wrong")
