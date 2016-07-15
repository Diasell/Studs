from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from ..models import BlogItemModel

from .serializers import (
    BlogItemDetailedSerializer,
    BlogItemShortSerializer
)

class BlogPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000



class BlogViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = BlogItemModel.objects.all()
    serializer_class = BlogItemShortSerializer
    pagination_class = BlogPagination

    def list(self, request):
        queryset = BlogItemModel.objects.all()
        serializer = BlogItemShortSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = BlogItemModel.objects.get(pk=pk)
        serializer = BlogItemDetailedSerializer(queryset)
        return Response(serializer.data)
