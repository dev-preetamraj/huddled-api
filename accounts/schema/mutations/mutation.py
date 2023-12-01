import graphene

from accounts.schema.mutations.profile_mutations import ProfileMutation
from accounts.schema.mutations.registration_mutation import RegistrationMutation
from django.contrib.auth import get_user_model

from accounts.schema.mutations.token_mutations import TokenMutation, RefreshTokenMutation, VerifyTokenMutation

User = get_user_model()


class AccountsMutation(graphene.ObjectType):
    register_user = RegistrationMutation.Field()
    auth_token = TokenMutation.Field()
    refresh_token = RefreshTokenMutation.Field()
    verify_token = VerifyTokenMutation.Field()
    update_profile = ProfileMutation.Field()
