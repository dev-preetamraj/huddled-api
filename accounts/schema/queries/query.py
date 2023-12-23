import logging
import graphene
from accounts.schema.types import UserType, DiscoverUserTypes
from django.contrib.auth import get_user_model
from accounts.decorators import login_required, admin_required

User = get_user_model()

# Get an instance of logger
logger = logging.getLogger('accounts')


class AccountsQuery(graphene.ObjectType):
    get_users = graphene.List(UserType)
    me = graphene.Field(UserType)
    suggested_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, user_id=graphene.String(required=True))
    discover_users = graphene.List(DiscoverUserTypes)

    @login_required
    @admin_required
    def resolve_get_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_suggested_users(self, info):
        user_id = info.context.user.id
        return User.objects.exclude(id=user_id)

    @login_required
    def resolve_user_by_id(self, info, user_id: str):
        user = User.objects.get(id=user_id)
        return user

    @login_required
    def resolve_discover_users(self, info):
        requested_user = info.context.user
        users = User.objects.all()
        data = []

        for user in users:
            friendship = requested_user.friends.filter(friend=user).first()
            discover_user = DiscoverUserTypes(
                user=user,
                friendship=friendship
            )
            data.append(discover_user)
        return data
