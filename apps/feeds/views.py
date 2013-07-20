import urllib
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from apps.feeds.models import *


class ArticleDetail(DetailView):
    model = Article

    def post(self, request, *args, **kwargs):
        set_read = request.POST.get('read')
        set_starred = request.POST.get('starred')
        update = {}
        if set_read is not None:
            update['unread'] = not (set_read == 'true')
        if set_starred is not None:
            update['starred'] = (set_starred == 'true')
        obj = self.get_object()
        Article.objects.filter(pk=obj.pk).update(**update)
        return HttpResponseRedirect(obj.url.default)


class ArticleList(ListView):
    model = Article

    def get_queryset(self):
        filtparms = {}
        params = self.kwargs.get('path_params')
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
