from django.contrib import admin

from .models import Post


class PostAdminConfig(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']


admin.site.register(Post, PostAdminConfig)
