from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from apps.news.models import News, Category
from apps.news.serializers import NewsSerializer, CategorySerializer


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path='count_news')
    def count_news(self, request, *args, **kwargs):
        category = self.get_object()
        count_news = News.objects.filter(category=category).count()
        return Response({'count_news': count_news})

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path='news_by_category')
    def news_by_category(self, request, *args, **kwargs):
        category = self.get_object()
        news = News.objects.filter(category_id=category.id)
        return Response(NewsSerializer(news, many=True).data)
