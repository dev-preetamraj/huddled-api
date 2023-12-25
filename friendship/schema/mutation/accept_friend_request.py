import logging

import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from accounts.decorators import login_required
from friendship.models import Friendship

User = get_user_model()

logger = logging.getLogger("friendship")


class AcceptFriendRequestMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    message = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, user_id: str):
        try:
            request_user = info.context.user
            friend_request_user = User.objects.get(id=user_id)
            friendship = Friendship.objects.filter(
                user=friend_request_user, friend=request_user, is_accepted=False
            ).first()
            if friendship:
                friendship.is_accepted = True
                friendship.save()
                Friendship.objects.create(
                    user=request_user, friend=friend_request_user, is_accepted=True
                )
                return AcceptFriendRequestMutation(message="Friend request accepted")
            return GraphQLError("No friendship found")
        except Exception as e:
            logger.error(f"AddFriendMutation error: {e}")
            raise GraphQLError("Something went wrong")
