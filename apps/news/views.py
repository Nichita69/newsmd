from django_filters import filters
from rest_framework.serializers import Serializer

from apps.news.task import  retrieve_news_task, get_comment_by_news_task, count_comments_task
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    NewsSerializer,
    NewsRetrieveSerializer,
    CategorySerializer,
    AttachmentSerializer,
    CommentSerializer
)
from .models import News, Category, Attachment, Comment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import parsers, renderers


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category_id', 'owner']
    ordering_fields = ['id']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        result = retrieve_news_task.delay(instance.id)
        data = result.get()
        if data:
            return Response(data)
        else:
            return Response({'error': 'News not found'}, status=404)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        return super(CategoryViewSet, self).get_permissions()


class AttachmentViewSet(ModelViewSet):
    serializer_class = AttachmentSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Attachment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['get'], serializer_class=CommentSerializer, url_path='comment_by_news')
    def comment_by_news(self, request, *args, **kwargs):
        news = self.get_object()
        result = get_comment_by_news_task.delay(news.id)
        data = result.get()
        return Response(data)

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path='count_comments')
    def count_comments(self, request, *args, **kwargs):
        news = self.get_object()
        # Вызов задачи count_comments_task асинхронно
        result = count_comments_task.delay(news.id)
        count_comments = result.get()
        return Response({'count_comments': count_comments})
