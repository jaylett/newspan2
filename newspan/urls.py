from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import apps.feeds.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', apps.feeds.views.LabelList.as_view()),
    url(r'^all(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.ArticleList.as_view()),
    url(r'^feed/(?P<pk>[0-9]+)(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.FeedDetail.as_view(), name='feed-detail'),
    url(r'^label/(?P<pk>[0-9]+)(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.LabelDetail.as_view(), name='label-detail'),
    url(r'^article/(?P<pk>[0-9]+)/$', apps.feeds.views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^admin/', include(admin.site.urls)),
)
