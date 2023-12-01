import graphene
from accounts.schema.types import UserType
from huddled.decorators import login_required
from enum import Enum


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
        first_name = graphene.String()
        middle_name = graphene.String()
        last_name = graphene.String()
        profile_picture = graphene.String()
        cover_picture = graphene.String()
        bio = graphene.String()
        mobile_number = graphene.String()
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
        user = info.context.user

        for key, value in kwargs.items():
            if key not in ['gender', 'relationship_status']:
                setattr(user, key, None if value == '' else value)
            else:
                setattr(user, key, value.value)

        user.save()

        return ProfileMutation(user=user)
