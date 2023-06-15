from django.urls import path
from rest_framework import routers

from apps.users.views import UserViewSet

# Create your patterns here.

app_name = "users"  # noqa

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="users")
# router.register(r"user", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    *router.urls,
]
