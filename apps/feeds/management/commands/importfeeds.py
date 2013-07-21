from apps.feeds.models import *
from django.core.management.base import BaseCommand
from zipfile import ZipFile
import urllib2
from bs4 import BeautifulSoup

class Command(BaseCommand):
    
    def file_is_an_xml_file(self, filename):
        return filename.endswith('xml')

    def get_or_not(self, element, aspect):
        if element.has_key(aspect):
            return element[aspect]
        return None

    def handle(self, *args, **options):
        filename = args[0]

        zfile = ZipFile(filename)

        exported_feeds_filename = [name for name in zfile.namelist() if self.file_is_an_xml_file(name)][0]

        feed_xml_content = zfile.read(exported_feeds_filename)

        soup = BeautifulSoup(feed_xml_content)

        all_outlines = soup.find_all('outline')



        for outline in all_outlines:
            if outline.has_key("type"):
                if outline["type"] == "rss":
                    
                    feed_url = self.get_or_not(outline, "xmlurl")
                    if feed_url is None:
                        feed_url = self.get_or_not(outline, "htmlurl")
                    
                    title = self.get_or_not(outline, "text")

                    print "%s: %s" % (title, feed_url)

                    if feed_url is not None and title is not None:
                        print "ok"
                        feed = Feed.objects.create(name=title, feed_url=feed_url)
                        feed.save()

            



