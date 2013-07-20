from datetime import datetime
import feedparser
import json
import time
from django.db import models
from django.utils import timezone


class Label(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Feed(models.Model):
    name = models.TextField()
    url = models.URLField(max_length=1024)
    last_updated = models.DateTimeField(null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(null=True, blank=True)
    last_contents = models.TextField(null=True, blank=True)
    labels = models.ManyToManyField(Label, null=True, blank=True, related_name='feeds')

    def _make_articles(self):
        """Create or update Article objects from entries in last_contents."""
        try:
            feed = feedparser.parse(self.last_contents)
            for entry in feed['entries']:
                try:
                    try:
                        article = Article.objects.get(guid=entry['id'])
                    except Article.DoesNotExist:
                        article = Article(guid=entry['id'], feed=self)
                    published = entry.get('published_parsed', None)
                    updated = entry.get('updated_parsed', None)
                    if not updated:
                        updated = published
                    if not published:
                        published = updated
                    if updated:
                        article.updated = datetime.fromtimestamp(time.mktime(updated), timezone.utc)
                    if published:
                        article.published = datetime.fromtimestamp(time.mktime(published), timezone.utc)
                    if 'published_parsed' in entry:
                        del entry['published_parsed']
                    if 'updated_parsed' in entry:
                        del entry['updated_parsed']
                    article.as_json = json.dumps(entry)
                    article.save()
                except Exception as e:
                    print "erm?"
                    import traceback
                    traceback.print_exc()
            self.last_update = timezone.now()
            self.last_error = None
            self.save()
        except Exception as e:
            self.last_error = str(e)
            raise

    def __unicode__(self):
        return self.name


class Article(models.Model):
    published = models.DateTimeField()
    updated = models.DateTimeField(null=True, blank=True)
    guid = models.TextField()
    feed = models.ForeignKey(Feed, related_name='articles')
    as_json = models.TextField()
    
    def __unicode__(self):
        return u"%s@%s" % (self.guid, unicode(self.feed))
