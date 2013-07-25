from django.contrib import admin

from apps.feeds.models import *


class LabelAdmin(admin.ModelAdmin):
    model = Label

    
class FeedAdmin(admin.ModelAdmin):
    model = Feed
    list_display = ['name', 'last_updated', 'all_labels']
    list_filter = ['labels']

    def all_labels(self, feed):
        return u", ".join(l.name for l in feed.labels.all())


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_filter = ['feed', 'unread', 'starred', 'feed__labels']


admin.site.register(Label, LabelAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, ArticleAdmin)
