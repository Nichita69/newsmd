import owner as owner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, parsers, renderers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from apps.news.models import News, Category, Comment, Attachment
from apps.news.serializers import NewsSerializer, CategorySerializer, CommentSerializer, NewsRetrieveSerializer, \
    AttachmentSerializer


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
        return Response(NewsRetrieveSerializer(instance).data)


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

    # @action(detail=True, methods=['get'], serializer_class=Serializer, url_path='comment_by_news')
    # def comment_by_news(self, request, *args, **kwargs):
    #     news = self.get_object()
    #     comment = Comment.objects.filter(news_id=news.id)
    #     return Response(CommentSerializer(comment, many=True).data)

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path='count_comments')
    def count_comments(self, request, *args, **kwargs):
        news = self.get_object()
        count_comments = Comment.objects.filter(news=news).count()
        return Response({'count_commets': count_comments})
