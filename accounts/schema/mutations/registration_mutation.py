import re

import graphene
from accounts.schema.types import UserType
from typing import Optional
from django.contrib.auth import get_user_model
from graphql import GraphQLError

User = get_user_model()


class RegistrationMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        first_name = graphene.String(default_value="")
        last_name = graphene.String(default_value="")
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, kwargs.get('email')):
            raise GraphQLError("Invalid email format")

        user_by_email = User.objects.filter(email=kwargs.get('email')).first()
        if user_by_email is not None:
            raise GraphQLError('User with this email already exists')

        user_by_username = User.objects.filter(username=kwargs.get('username')).first()
        if user_by_username is not None:
            raise GraphQLError('User with this username already exists')

        if len(kwargs.get('password')) < 8:
            raise GraphQLError('Password must be 8 or more characters long')

        if kwargs.get('password') != kwargs.get('confirm_password'):
            raise GraphQLError('Password did not matched')

        try:
            user = User.objects.create_user(
                email=kwargs.get('email'),
                username=kwargs.get('username'),
                first_name=kwargs.get('first_name'),
                last_name=kwargs.get('last_name'),
                password=kwargs.get('password')
            )
        except Exception as e:
            print(e)
            raise GraphQLError('Something went wrong')
        return RegistrationMutation(user=user)