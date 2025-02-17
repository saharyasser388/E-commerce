from django.http import JsonResponse
from strawberry.django.views import GraphQLView
from .schema import schema



graphql_view = GraphQLView.as_view(schema=schema)