from apps.feeds.models import *
from django.core.management.base import BaseCommand
import urllib2
import listparser


class Command(BaseCommand):
    
    def file_is_an_xml_file(self, filename):
        return filename.endswith('xml')

    def get_or_not(self, element, aspect):
        if element.has_key(aspect):
            return element[aspect]
        return None

    def handle(self, *args, **options):
        opml_file = open(args[0])
        opml = listparser.parse( opml_file )
        
        for feed in opml.feeds:
            print "%s: %s" % ( feed.title, feed.url )
            feed_object = Feed.objects.create(
                name=feed.title,
                feed_url=feed.url,
            )
            feed_object.save()
            for tag in feed.tags:
                # .get_or_create() with a name that begins with a number
                # (eg. '0-premium') causes .add() to break: "TypeError: int()
                # argument must be a string or a number, not 'Label'" so
                # we fetch the label again. Le sigh.
                label = Label.objects.get_or_create(name=tag)
                label = Label.objects.get(name=tag)
                feed_object.labels.add(label)
