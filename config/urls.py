from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="NEWS API",
        default_version='v1',
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/', include('apps.users.urls')),
    path('news/', include('apps.news.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
