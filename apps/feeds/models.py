from datetime import datetime
import feedparser
import json
import time
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from lib.urlattr import UrlAttr, UrlAttrMixin


feedparser._HTMLSanitizer.acceptable_elements.add('iframe')


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
            self.last_updated = timezone.now()
            self.last_error = None
            self.save()
        except Exception as e:
            self.last_error = str(e)
            self.save()
            raise

    def __unicode__(self):
        return self.name


class Article(models.Model, UrlAttrMixin):
    published = models.DateTimeField()
    updated = models.DateTimeField(null=True, blank=True)
    guid = models.TextField()
    feed = models.ForeignKey(Feed, related_name='articles')
    as_json = models.TextField()
    starred = models.BooleanField(default=False, help_text='Starred by the HUMAN')
    unread = models.BooleanField(default=True, help_text='Unread by the HUMAN')

    _as_dict = None
    
    @property
    def entry(self):
        if self._as_dict is None:
            self._as_dict = json.loads(self.as_json)
        return self._as_dict

    def title(self):
        # may be HTML or text...
        return mark_safe(self.entry['title'])

    def authors(self):
        if 'authors' in self.entry:
            return self.entry['authors']
        elif 'author_detail' in self.entry:
            return [self.entry['author_detail']]
        elif 'author' in self.entry:
            return [{
                'name': self.entry['author'],
            }]
        else:
            return []

    def body(self):
        candidates = []
        def is_viable(content):
            if content['type'] in ['text', 'html', 'xhtml', 'application/xhtml+xml', ]:
                return True
            if content['type'].startswith('text/'):
                return True
            return False
        candidates = filter(is_viable, self.entry['content'])
        for candidate in candidates:
            if candidate['type'] == 'text' or candidate['type'].startswith('text/'):
                candidate['_SCORE'] = 1
            elif candidate['type'] in ['html', 'xhtml', 'text/html', 'application/xhtml+xml']:
                candidate['_SCORE'] = 2
        candidates.sort(key=lambda x: x['_SCORE'], reverse=True)

        content = None

        if len(candidates) > 0:
            content = candidates[0]
        elif 'summary_detail' in self.entry:
            content = self.entry['summary_detail']
        elif 'summary' in self.entry:
            content = {
                'value': self.entry['summary'],
                'type': 'html', # probably?
            }

        if content is None:
            return None

        if content['type'] in ['html', 'xhtml', 'text/html', 'application/xhtml+xml']:
            content['value'] = mark_safe(content['value'])

        return content
    
    class Meta:
        ordering = ('-updated',)

    url = UrlAttr(
        default='article-detail=',
    )

    def __unicode__(self):
        return u"%s@%s" % (self.guid, unicode(self.feed))
