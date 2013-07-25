from apps.feeds.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            feed.update()
