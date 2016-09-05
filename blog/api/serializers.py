from rest_framework import serializers

from ..models import BlogItemModel, CommentModel


class BlogItemShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogItemModel
        fields = (
            'pk',
            "title",
            'title_image',
            "updated"
        )


class BlogItemDetailedSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.last_name',
        read_only=True
    )

    class Meta:
        model = BlogItemModel
        fields = (
            'title',
            'title_image',
            'author',
            'content',
            'created',
            'updated'
        )


class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentModel
        fields = (
            'id',
            'user',
            'comment',
            'created',
            'updated',
            'blog_post',
            'is_removed',
            'is_visible'
        )
