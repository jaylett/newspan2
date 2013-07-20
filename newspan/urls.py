from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import apps.feeds.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', apps.feeds.views.ArticleList.as_view()),
    url(r'^all(?P<path_params>;[.;=,\w\d\-\_]*)?/$', apps.feeds.views.ArticleList.as_view()),
    url(r'^article/(?P<pk>[0-9]+)/$', apps.feeds.views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^admin/', include(admin.site.urls)),
)
