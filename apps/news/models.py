from django.contrib.auth.models import User

from apps.common.models import BaseModel
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)


class News(models.Model):
    title = models.CharField(max_length=255, null=True)
    content = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
