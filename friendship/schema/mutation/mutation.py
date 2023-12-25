import graphene

from friendship.schema.mutation.accept_friend_request import AcceptFriendRequestMutation
from friendship.schema.mutation.add_friend import AddFriendMutation


class FriendshipMutation(graphene.ObjectType):
    add_friend = AddFriendMutation.Field()
    accept_friend_request = AcceptFriendRequestMutation.Field()
