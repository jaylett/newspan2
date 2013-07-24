import logging
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login_required
from django.views.generic import TemplateView

import apps.feeds.views
from newspan.forms import AuthenticationForm

from django.contrib import admin
admin.autodiscover()

logger = logging.getLogger('django')

urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'authentication_form': AuthenticationForm}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)

def protected_urls(prefix, *args):
    def protected(u):
        u = list(u)
        u[1] = login_required(u[1])
        return tuple(u)

    return patterns(
        prefix,
        *[protected(u) for u in args]
    )

urlpatterns += protected_urls(
    '',
    (r'^$', apps.feeds.views.LabelList.as_view(), {}, 'home'),
    (r'^all(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.ArticleList.as_view(), {}),
    (r'^feed/(?P<pk>[0-9]+)(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.FeedDetail.as_view(), {}, 'feed-detail'),
    (r'^label/(?P<pk>[0-9]+)(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.LabelDetail.as_view(), {}, 'label-detail'),
    (r'^all(?P<path_params>;[.;=,\w\d\-\_]*)?/article/(?P<article_pk>[0-9]+)/$', apps.feeds.views.ArticleInAll.as_view()),
    (r'^feed/(?P<pk>[0-9]+)(?P<path_params>;[.;=,\w\d\-\_]*)?/article/(?P<article_pk>[0-9]+)/$', apps.feeds.views.ArticleInFeed.as_view(), {}, 'feed-detail'),
    (r'^label/(?P<pk>[0-9]+)(?P<path_params>;[.;=,\w\d\-\_]*)?/article/(?P<article_pk>[0-9]+)/$', apps.feeds.views.ArticleInLabel.as_view(), {}, 'label-detail'),
    (r'^article/(?P<pk>[0-9]+)/$', apps.feeds.views.ArticleDetail.as_view(), {}, 'article-detail'),
)
