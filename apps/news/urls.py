from rest_framework import routers
from apps.news.views import NewsViewSet, CategoryViewSet

router = routers.SimpleRouter(trailing_slash=False)


router.register(r'news', NewsViewSet, basename='news')
router.register('category',CategoryViewSet,basename='category')
urlpatterns = [
    *router.urls,
]
