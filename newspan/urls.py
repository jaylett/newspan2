from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import apps.feeds.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', apps.feeds.views.ArticleList.as_view()),
    url(r'^article/(?P<pk>[0-9]+)/$', apps.feeds.views.ArticleDetail.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
