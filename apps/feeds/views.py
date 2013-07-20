from django.views.generic import DetailView
from apps.feeds.models import *


class ArticleDetail(DetailView):
    model = Article
