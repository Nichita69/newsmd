import os
from pathlib import Path

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.common.models import BaseModel


def upload_to(instance, filename: str) -> str:
    return Path(str(instance.owner_id)).joinpath(filename).as_posix()


class Category(BaseModel):
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)


class News(BaseModel):
    title = models.CharField(max_length=255, null=True)
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_publish = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_to)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Comment(BaseModel):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class Attachment(BaseModel):
    file_upload = models.FileField(
        upload_to="foo/",
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "jpg", "png"]
        )
        ]
    )
    title = models.CharField(max_length=255, null=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_size = models.IntegerField(default=0)

    def save(self, **kwargs):
        if not self.file_size:
            self.file_size = self.file_upload.size
            super().save(**kwargs)

    @property
    def extension(self) -> str:
        name, extension = os.path.splitext(self.file_upload.name)
        return extension

    class Timer(BaseModel):
        news = models.ForeignKey(News, on_delete=models.CASCADE)
        is_stopped = models.BooleanField(default=False)
        is_running = models.BooleanField(default=False)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
