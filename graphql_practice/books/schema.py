# Describes data models for SQL server
import graphene 
from graphene_django import DjangoObjectType

from .models import Books, Authors
# modeling output int terms of graph structure 
class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "name", "excerpt")

class AuthorsType(DjangoObjectType):
    class Meta:
        model = Authors
        fields = ("id", "name", "field")

class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType, name=graphene.String())
    all_authors = graphene.List(AuthorsType)

    #Filter by Auther name or leave blank
    def resolve_all_books(root,info, name =None):
        if name: return Books.objects.filter(name=name)
        else: return Books.objects.all()
    def resolve_all_authors(self, info):
        return Authors.objects.all()
schema = graphene.Schema(query=Query)

