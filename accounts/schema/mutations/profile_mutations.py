import logging
from enum import Enum

import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from accounts.decorators import login_required
from accounts.schema.types import UserNode

# Get an instance of logger
logger = logging.getLogger("accounts")

User = get_user_model()


class GenderEnum(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHERS = "Others"
    NONE = None


class RelationshipEnum(Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    COMPLICATED = "Complicated"
    NONE = None


class ProfileMutation(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String()
        bio = graphene.String()
        gender = graphene.Argument(graphene.Enum.from_enum(GenderEnum))
        relationship_status = graphene.Argument(
            graphene.Enum.from_enum(RelationshipEnum)
        )
        street = graphene.String()
        city = graphene.String()
        state = graphene.String()
        postal_code = graphene.String()
        country = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        try:
            user = info.context.user
            for key, value in kwargs.items():
                if key in ["gender", "relationship_status"]:
                    setattr(user, key, value.value)
                elif key == "username":
                    is_username_unique = not User.objects.filter(
                        username=value
                    ).exists()
                    if is_username_unique:
                        setattr(user, key, None if value == "" else value)
                    else:
                        return GraphQLError("Username not available")
                else:
                    setattr(user, key, None if value == "" else value)

            user.save()
        except Exception as e:
            logger.error(f"ProfileMutation : {e}")
            raise GraphQLError("Something went wrong")

        return ProfileMutation(user=user)
