from celery import shared_task

from apps.news.models import News, Comment
from apps.news.serializers import NewsRetrieveSerializer, CommentSerializer


@shared_task
def retrieve_news_task(news_id):
    try:
        news = News.objects.get(id=news_id)
        data = NewsRetrieveSerializer(news).data
        return data
    except News.DoesNotExist:
        return None


@shared_task
def get_comment_by_news_task(news_id):
    comments = Comment.objects.filter(news_id=news_id)
    data = CommentSerializer(comments, many=True).data
    return data


@shared_task
def count_comments_task(news_id):
    count_comments = Comment.objects.filter(news_id=news_id).count()
    return count_comments
