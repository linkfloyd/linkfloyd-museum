from django.contrib import admin
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ("posted_by", "link", "posted_at")

admin.site.register(Comment, CommentAdmin)
