from django.db import models


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
