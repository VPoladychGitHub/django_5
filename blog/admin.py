from django.utils import timezone

from django.contrib import admin
from django.core.checks import messages
from django.utils.translation import ngettext
from django.contrib import messages
from .models import Article, Comment, Author, AuthorProfile


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_text', 'comment_status']
    ordering = ['comment_text']
    actions = ['make_published']

    def make_published(self, request, queryset):
        updated = queryset.update(comment_status=Comment.CommentStatus.PUBLISHED)
        self.message_user(request, ngettext(
            '%d Comment was successfully marked as published.',
            '%d Comment were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Mark selected comment as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_status', 'published_date']
    ordering = ['title']
    actions = ['make_published']

    def make_published(self, request, queryset):
        updated = queryset.update(post_status='published', published_date=timezone.now())
        self.message_user(request, ngettext(
            '%d Article was successfully marked as published.',
            '%d Articles were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Mark selected article as published"


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author)
admin.site.register(AuthorProfile)
