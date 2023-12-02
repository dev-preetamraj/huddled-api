import logging
import graphene
from accounts.schema.types import UserType
from django.contrib.auth import get_user_model
from accounts.decorators import login_required, admin_required

User = get_user_model()

# Get an instance of logger
logger = logging.getLogger('accounts')


class AccountsQuery(graphene.ObjectType):
    get_users = graphene.List(UserType)
    me = graphene.Field(UserType)

    @login_required
    @admin_required
    def resolve_get_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_me(self, info):
        return info.context.user
