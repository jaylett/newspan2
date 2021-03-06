from datetime import datetime
import feedparser
import json
import time
import urllib2
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from lib.urlattr import UrlAttr, UrlAttrMixin


feedparser._HTMLSanitizer.acceptable_elements.add('iframe')


class ArticleCountingMixin(object):

    def unread_articles(self):
        return self.articles.filter(unread=True)

    def starred_articles(self):
        return self.articles.filter(starred=True)


class Label(models.Model, UrlAttrMixin, ArticleCountingMixin):
    name = models.CharField(max_length=128)

    @property
    def articles(self):
        return Article.objects.filter(feed__labels=self).distinct()

    url = UrlAttr(
        default='label-detail=',
    )

    def __unicode__(self):
        return self.name


class Feed(models.Model, UrlAttrMixin, ArticleCountingMixin):
    name = models.TextField(blank=True)
    feed_url = models.URLField(max_length=1024, db_column='url')
    last_updated = models.DateTimeField(null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(null=True, blank=True)
    last_contents = models.TextField(null=True, blank=True)
    labels = models.ManyToManyField(Label, null=True, blank=True, related_name='feeds')

    _parsed_contents = None
    
    @property
    def parsed_contents(self):
        if self._parsed_contents is None:
            self._parsed_contents = feedparser.parse(self.last_contents)
        return self._parsed_contents

    def authors(self):
        feed = self.parsed_contents.get('feed', {})
        if 'authors' in feed and len(feed['authors']) and feed['authors'][0]!={}:
            return feed['authors']
        elif 'author_detail' in feed:
            return [feed['author_detail']]
        elif 'author' in feed and feed['author']:
            return [{
                'name': feed['author'],
            }]
        else:
            return []

    def update(self):
        self.last_checked = timezone.now()
        try:
            response = urllib2.urlopen(self.feed_url)
            charset = 'utf8' # sensible default
            ctype_bits = response.info().get('content-type', 'text/xml').split(';')
            if len(ctype_bits) > 1:
                args = dict([s.lower() for s in kv.split('=')] for kv in ctype_bits[1:])
                charset = args.get('charset', charset)
            else:
                pass
            contents = response.read()
            try:
                contents = contents.decode(charset)
            except UnicodeDecodeError:
                try:
                    contents = contents.decode('utf8')
                except UnicodeDecodeError:
                    contents = contents.decode('iso-8859-1')
            self.last_contents = contents
            self._make_articles()
        except Exception as e:
            self.last_error = str(e)
            print u"%s failed to update: %s" % (self.name, str(e))
        finally:
            self.save()
        

    def _make_articles(self):
        """Create or update Article objects from entries in last_contents."""
        try:
            feed = feedparser.parse(self.last_contents)
            if 'feed' in feed and 'title_detail' in feed['feed'] and not self.name:
                title = feed['feed']['title_detail']
                if title['type'] != 'text/plain':
                    # HTML, we should strip tags and unescape
                    pass
                self.name = title['value']
            for entry in feed['entries']:
                try:
                    guid = entry.get('id')
                    if guid is None:
                        #print "Hmm, no guid for this entry?\n%s" % str(entry)
                        guid = entry.get('link')
                    if guid is None:
                        # nothing we can reasonably do
                        continue
                    try:
                        article = Article.objects.get(guid=guid)
                    except Article.DoesNotExist:
                        article = Article(guid=guid, feed=self)
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
                    elif article.id is None:
                        # make it now!
                        article.published = timezone.now()
                        #print "Hmm, no published date for this entry from %s?\n%s" % (self.name, str(entry))
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

    url = UrlAttr(
        default='feed-detail=',
    )

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

    def link(self):
        return self.entry['link']

    def authors(self):
        if 'authors' in self.entry and len(self.entry['authors']) and self.entry['authors'][0]!={}:
            return self.entry['authors']
        elif 'author_detail' in self.entry:
            return [self.entry['author_detail']]
        elif 'author' in self.entry and self.entry['author']:
            return [{
                'name': self.entry['author'],
            }]
        else:
            return self.feed.authors()

    def body(self):
        candidates = []
        def is_viable(content):
            if content['type'] in ['text', 'html', 'xhtml', 'application/xhtml+xml', ]:
                return True
            if content['type'].startswith('text/'):
                return True
            return False
        candidates = filter(is_viable, self.entry.get('content', []))
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
        ordering = ('-updated', '-pk')

    url = UrlAttr(
        default='article-detail=',
    )

    def __unicode__(self):
        return u"%s@%s" % (self.guid, unicode(self.feed))
