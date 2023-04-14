from django.db import models
from django.utils.text import slugify
from django_editorjs import EditorJsField
from django_quill.fields import QuillField


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = EditorJsField()

    def __str__(self):
        return self.title


class QuillPost(models.Model):
    title = models.TextField(max_length=180)
    description = models.TextField(max_length=180)
    content = QuillField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(QuillPost, self).save(*args, **kwargs)
