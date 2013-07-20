from django.views.generic import DetailView, ListView
from apps.feeds.models import *


class ArticleDetail(DetailView):
    model = Article


class ArticleList(ListView):
	model = Article