from django.http import JsonResponse
from strawberry.django.views import GraphQLView
from django.urls import path
from .schema import schema
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

graphql_view = GraphQLView.as_view(schema=schema)


urlpatterns = [
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))),
]