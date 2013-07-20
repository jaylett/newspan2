from apps.feeds.models import *
from django.utils import timezone
from django.core.management.base import BaseCommand
import urllib2

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            feed.last_checked = timezone.now()
            try:
                response = urllib2.urlopen(feed.url)
                feed.last_contents = response.read()
                feed.save()
                feed._make_articles()
            except Exception as e:
                feed.last_error = str(e)
                feed.save()
            



