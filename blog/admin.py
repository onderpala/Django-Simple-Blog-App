from django.contrib import admin

# Register your models here.

from .models import Post, PostTag, PostCategory, PostComment

admin.site.register(Post)
admin.site.register(PostTag)
admin.site.register(PostCategory)
admin.site.register(PostComment)