from typing import TYPE_CHECKING

import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from blog import models

if TYPE_CHECKING:
    from graphql import ResolveInfo


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Profile


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag


class Query(graphene.ObjectType):

    # This class will bring together all the type classes, and all the methods added to it to indicate
    # the ways in which the models can be queried

    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    def resolve_all_posts(root, info: "ResolveInfo"):
        return (
            models.Post.objects.prefetch_related("tags").select_related("author").all()
        )

    def resolve_author_by_username(root, info: "ResolveInfo", username: str):
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

    def resolve_post_by_slug(root, info: "ResolveInfo", slug: str):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info: "ResolveInfo", username: str):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_tag(root, info: "ResolveInfo", tag: str):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )


# The created GRAPHENE variable created points to blog.schema.schema.
# This schema variable wraps the Query class in graphene.Schema to tie all together
schema = graphene.Schema(query=Query)
