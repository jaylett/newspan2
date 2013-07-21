import urllib
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from apps.feeds.models import *


class LabelList(ListView):
    model = Label

    def get_context_data(self, **kwargs):
        context = {
            'unlabelled_feeds': Feed.objects.filter(labels__pk__isnull=True),
        }
        context.update(kwargs)
        return super(LabelList, self).get_context_data(**context)


class MarkArticleMixin(object):

    def post(self, request, *args, **kwargs):
        set_read = request.POST.get('read')
        set_starred = request.POST.get('starred')
        update = {}
        if set_read is not None:
            update['unread'] = not (set_read == 'true')
        if set_starred is not None:
            update['starred'] = (set_starred == 'true')
        obj = self.get_article_object()
        Article.objects.filter(pk=obj.pk).update(**update)
        return HttpResponseRedirect(request.get_full_path())


class ArticleDetail(MarkArticleMixin, DetailView):
    model = Article

    def get_article_object(self):
        return self.get_object()

    def get_context_data(self, **kwargs):
        context = {
            'base_url': '/',
        }
        context.update(kwargs)
        return super(ArticleDetail, self).get_context_data(**context)


class ArticleFilterMixin(object):

    def get_filtered_set(self):
        filtparms = {}
        params = self.kwargs.get('path_params')
        if params is None:
            self.path_params = ''
        else:
            self.path_params = params
        _kwargs = {}
        if params is not None:
            bits = params.split(';')
            for b in bits:
                if b == '':
                    # first one with nothing before it
                    continue
                pieces = map(lambda x: urllib.unquote_plus(x), b.split('='))
                if pieces[0] == '':
                    continue
                if len(pieces)==2:
                    _kwargs[pieces[0]] = pieces[1]
                elif len(pieces)==1:
                    _kwargs[pieces[0]] = True
                else:
                    # very weird, but let's not just throw up
                    _kwargs[pieces[0]] = '='.join(pieces[1:])

        show = _kwargs.get('show', 'unread')
        if show == 'starred':
            filtparms['starred'] = True
        elif show == 'unread':
            filtparms['unread'] = True
        
        return Article.objects.filter(**filtparms)

    def post(self, request, *args, **kwargs):
        if hasattr(self, 'get_object'):
            self.object = self.get_object()
        set_read = self.request.POST.get('read')
        if set_read is not None:
            self.get_filtered_set().update(
                unread = not (set_read == 'true'),
            )
        return HttpResponseRedirect(request.get_full_path())


class ArticleList(ArticleFilterMixin, ListView):
    model = Article

    def get_queryset(self):
        return self.get_filtered_set()

    def get_context_data(self, **kwargs):
        context = {
            'base_url': '/all' + self.path_params + '/',
        }
        context.update(kwargs)
        return super(ArticleList, self).get_context_data(**context)


class FeedDetail(ArticleFilterMixin, DetailView):
    model = Feed

    def get_filtered_set(self):
        queryset = super(FeedDetail, self).get_filtered_set()
        return queryset.filter(feed=self.object)

    def get_context_data(self, **kwargs):
        context = {
            'object_list': self.get_filtered_set(),
            'base_url': '/feed/' + str(self.object.pk) + self.path_params + '/',
        }
        context.update(kwargs)
        return super(FeedDetail, self).get_context_data(**context)


class LabelDetail(ArticleFilterMixin, DetailView):
    model = Label

    def get_filtered_set(self):
        queryset = super(LabelDetail, self).get_filtered_set()
        return queryset.filter(feed__labels=self.object).distinct()

    def get_context_data(self, **kwargs):
        context = {
            'object_list': self.get_filtered_set(),
            'base_url': '/label/' + str(self.object.pk) + self.path_params + '/',
        }
        context.update(kwargs)
        return super(LabelDetail, self).get_context_data(**context)


class NextArticleMixin(object):

    def get_article_object(self):
        return get_object_or_404(Article, pk=self.kwargs['article_pk'])

    def get_context_data(self, **kwargs):
        article = kwargs['article']
        context = {}
        try:
            next_article = (self.get_filtered_set().filter(
                updated__lt=article.updated
            ) | self.get_filtered_set().filter(
                updated=article.updated,
                pk__lt=article.pk,
            ))[0]
            context['next_article'] = next_article
        except IndexError:
            pass
        context.update(kwargs)
        return super(NextArticleMixin, self).get_context_data(**context)


class ArticleInAll(MarkArticleMixin, NextArticleMixin, ArticleList):
    template_name = 'feeds/article_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'article': self.get_article_object(),
        }
        context.update(kwargs)
        return super(ArticleInAll, self).get_context_data(**context)


class ArticleInFeed(MarkArticleMixin, NextArticleMixin, FeedDetail):
    template_name = 'feeds/article_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'article': self.get_article_object(),
        }
        context.update(kwargs)
        return super(ArticleInFeed, self).get_context_data(**context)


class ArticleInLabel(MarkArticleMixin, NextArticleMixin, LabelDetail):
    template_name = 'feeds/article_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'article': self.get_article_object(),
        }
        context.update(kwargs)
        return super(ArticleInLabel, self).get_context_data(**context)
