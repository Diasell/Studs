from rest_framework import serializers

from ..models import BlogItemModel


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
