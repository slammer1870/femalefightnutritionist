from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField


class Post(models.Model):
    title = models.TextField(max_length=180, unique=True)
    description = models.TextField(max_length=180)
    content = QuillField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
