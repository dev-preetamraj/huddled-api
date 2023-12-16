import logging
import graphene
from graphql import GraphQLError
from accounts.schema.types import UserType
from accounts.decorators import login_required
from enum import Enum

# Get an instance of logger
logger = logging.getLogger('accounts')


class GenderEnum(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others',
    NONE = None


class RelationshipEnum(Enum):
    SINGLE = 'Single'
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    COMPLICATED = 'Complicated',
    NONE = None


class ProfileMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        cover_picture = graphene.String()
        bio = graphene.String()
        gender = graphene.Argument(graphene.Enum.from_enum(GenderEnum))
        relationship_status = graphene.Argument(graphene.Enum.from_enum(RelationshipEnum))
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
                if key not in ['gender', 'relationship_status']:
                    setattr(user, key, None if value == '' else value)
                else:
                    setattr(user, key, value.value)

            user.save()
        except Exception as e:
            logger.error(f'ProfileMutation : {e}')
            raise GraphQLError('Something went wrong')

        return ProfileMutation(user=user)
