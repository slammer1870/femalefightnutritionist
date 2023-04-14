from django.contrib import admin

from .models import Post


@admin.register(Post)
class QuillPostAdmin(admin.ModelAdmin):
    exclude = ['slug',]
    pass
