from django.contrib import admin

from .models import Post, QuillPost


@admin.register(QuillPost)
class QuillPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post)
