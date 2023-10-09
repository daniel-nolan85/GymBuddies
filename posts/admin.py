from django.contrib import admin

from .models import Category, Post, Comment, HighFive


class AdminPost(admin.ModelAdmin):
    list_filter = ['created']
    list_display = ['short_content', 'created']
    search_fields = ['content']

    class Meta:
        model = Post


class AdminComment(admin.ModelAdmin):
    list_filter = ['created']
    search_fields = ['content']

    class Meta:
        model = Comment


admin.site.register(Category)
admin.site.register(Post, AdminPost)
admin.site.register(Comment, AdminComment)
admin.site.register(HighFive)
