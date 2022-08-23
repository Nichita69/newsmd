from rest_framework import routers
from apps.news.views import NewsViewSet, CategoryViewSet, CommentViewSet, AttachmentViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'news', NewsViewSet, basename='news')
router.register('category', CategoryViewSet, basename='category')
router.register('comment', CommentViewSet, basename='comment')
router.register('attachment', AttachmentViewSet, basename='attachment')
urlpatterns = [
    *router.urls,
]
