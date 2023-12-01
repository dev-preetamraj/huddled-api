import graphene
from accounts.schema.queries.query import AccountsQuery
from accounts.schema.mutations.mutation import AccountsMutation


class Query(AccountsQuery, graphene.ObjectType):
    pass


class Mutation(AccountsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
