from django.contrib.auth.models import User
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, parsers, renderers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from apps.news.models import (
    News,
    Category,
    Comment,
    Attachment
)
from apps.news.serializers import (
    NewsSerializer,
    CategorySerializer,
    CommentSerializer,
    NewsRetrieveSerializer,
    AttachmentSerializer
)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy', 'partial_update'):
            self.permission_classes = (IsAdminUser,)
        return super(CategoryViewSet, self).get_permissions()


class NewsViewSet(ModelViewSet):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category_id', 'owner']
    ordering_fields = ['id', 'created_at']
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance: News = self.get_object()
        user: User = request.user

        if user.id not in instance.members.values('id'):
            instance.members.add(user)
            instance.total_views = instance.members.count()

        instance.save()

        return Response(NewsRetrieveSerializer(instance).data)


class AttachmentViewSet(ModelViewSet):
    serializer_class = AttachmentSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Attachment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        if not self.request.user.is_anonymous:
            return self.queryset.filter(owner=self.request.user)

        return super(AttachmentViewSet, self).get_queryset()

    # def get_queryset(self):
    #


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path='count_comments')
    def count_comments(self, request, *args, **kwargs) -> Response:
        news = self.get_object()
        count_comments = Comment.objects.filter(news=news).count()
        return Response({'count_comments': count_comments})


    # @action(detail=True,methods=['post'],serializer_class=Serializer,url_path='adauga_comments')

