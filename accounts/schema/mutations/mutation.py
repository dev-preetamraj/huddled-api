import graphene
from accounts.schema.mutations.profile_mutations import ProfileMutation
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsMutation(graphene.ObjectType):
    update_profile = ProfileMutation.Field()
