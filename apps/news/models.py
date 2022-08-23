import os
from pathlib import Path

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from pip._internal.cli.spinners import open_spinner

from apps.common.models import BaseModel
from django.db import models


def upload_to(instance, filename):
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

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Comment(BaseModel):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class Attachment(BaseModel):
    file = models.FileField( upload_to="foo/", validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    title = models.CharField(max_length=255, null=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def extension(self):
        return self

