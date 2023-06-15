from timeit import Timer

from django.contrib import admin

from django.db.models import Q
from django.template.defaultfilters import filesizeformat
from django_filters import DateRangeFilter, DateTimeFromToRangeFilter

from apps.news.models import News, Attachment, Comment, Category


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'owner', 'is_publish', 'total_views')
    list_filter = ('title', 'owner', 'is_publish',
                   ('updated_at'),

                   )

class ExtensionListFilter(admin.SimpleListFilter):
    title = ('file extension')

    parameter_name = 'extension'

    def lookups(self, request, model_admin):
        return (
            ('.jpg', 'jpg'),
            ('.png', 'png'),
            ('.pdf', 'pdf'),
            ('.xlsx', 'xlsx'),
            ('.doc', 'doc'),
            ('.exe', 'exe'),
            ('.txt', 'txt'),
            ('.csv', 'csv'),
            ('other', 'other'),
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'other':
                return queryset.filter(
                    ~Q(file_upload__icontains='.jpg') & ~Q(file_upload__icontains='.pdf') & ~Q(
                        file_upload__icontains='.png') & ~Q(file_upload__icontains='.xlsx') & ~Q(
                        file_upload__icontains='.doc') & ~Q(file_upload__icontains='.exe') & ~Q(
                        file_upload__icontains='.txt') & ~Q(file_upload__icontains='.csv'))
            return queryset.filter(file_upload__icontains=self.value())
        return queryset


class SizeListFilter(admin.SimpleListFilter):
    title = ('file size')

    parameter_name = 'size'

    def lookups(self, request, model_admin):
        return (
            ('< 1MB', ('< 1MB')),
            ('1MB - 5Mb', ('1MB - 5Mb')),
            ('> 5Mb', ('> 5Mb')),
        )

    def queryset(self, request, queryset):
        if self.value() == '< 1MB':
            return queryset.filter(file_size__lte=1048576)
        if self.value() == '1MB - 5Mb':
            return queryset.filter(file_size__gt=1048576, file_size__lte=5242880)
        if self.value() == '10MB> 5Mb':
            return queryset.filter(file_size__gt=5242880)
        if self.value() == '> 10Mb':
            return queryset.filter(file_size__gt=52428800)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_upload', 'id', 'title', 'public', 'owner', 'extension')
    list_filter = (SizeListFilter, ExtensionListFilter, 'owner', 'title', 'public')
    ordering = ('id',)

    @staticmethod
    def size(obj):
        return filesizeformat(obj.file_size)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'news')
    list_filter = ('user', 'news')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class TimerUserFilter(admin.SimpleListFilter):
    title = ('user')

    parameter_name = 'user'

    def lookups(self, request, model_admin):
        return (
            ('user', 'user'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user=self.value())
        return queryset

# @admin.register(Timer)
# class TimerAdmin(admin.ModelAdmin):
#     list_display = ('news', 'user')
