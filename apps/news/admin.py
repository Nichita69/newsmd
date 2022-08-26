from django.contrib import admin

from apps.news.models import News, Attachment, Comment, Category


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'owner', 'is_publish', 'total_views')
    list_filter = ('title', 'owner', 'is_publish', 'created_at', 'total_views')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file', 'id', 'title', 'public', 'owner', 'extension')
    list_filter = ('owner', 'title', 'public')
    ordering = ('id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'news')
    list_filter = ('user', 'news')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
