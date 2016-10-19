from rest_framework import status, views, viewsets
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,
)
from ..models import BlogItemModel

from .serializers import (
    BlogItemDetailedSerializer,
    BlogItemShortSerializer,
    #CommentModelSerializer
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


# class AddCommentView(views.APIView):
#     """
#     API endpoint that allows user to add comments to blog items.
#     """
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = CommentModelSerializer
#
#     def post(self, request):
#         user = request.user
#         comment = request.data['comment']
#         blog_title = request.data['blog_post']
#
#         blog_item = BlogItemModel.objects.filter(title=blog_title)[0]
#
#         if user.is_active and blog_item:
#             new_comment = CommentModel.objects.create(
#                 blog_post=blog_item,
#                 comment=comment,
#                 user=user
#             )
#             new_comment.save()
#             return Response({'success': 'Comment has been saved'},
#                             status=status.HTTP_201_CREATED)
#         else:
#             return Response({"UnAuth": "Current user is not active"},
#                             status=status.HTTP_401_UNAUTHORIZED)
#
#
# class ListCommentsForItem(views.APIView):
#     """
#     API endpoint that allows to get all comments for given blog item
#     """
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     # serializer_class =
#
#     def post(self, request):
#         user = request.user
#         blog_title = request.data['title']
#
#         blog_item = BlogItemModel.objects.filter(title=blog_title)[0]
#
#         if user.is_active and blog_item:
#             response = dict()
#
#             return Response({'success': 'Comment has been saved'},
#                             status=status.HTTP_201_CREATED)
#         else:
#             return Response({"UnAuth": "Current user is not active"},
#                             status=status.HTTP_401_UNAUTHORIZED)

