import graphene
from accounts.schema.queries.query import AccountsQuery
from accounts.schema.mutations.mutation import AccountsMutation
from friendship.schema.query.query import FriendshipQuery
from friendship.schema.mutation.mutation import FriendshipMutation


class Query(AccountsQuery, FriendshipQuery, graphene.ObjectType):
    pass


class Mutation(AccountsMutation, FriendshipMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
