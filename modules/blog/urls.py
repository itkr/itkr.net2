# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (BlogListView, EntryDetailView, FeatureView, IndexView,
                    TagListView, TagView)

PREFIX = 'blog'

urlpatterns = [
    # all
    url(r'^$', IndexView.as_view(), name=PREFIX),
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^(?P<page>\d+)$', IndexView.as_view(), name=PREFIX),
    # feature
    url(r'^feature/(?P<blog_id>\d+)$', FeatureView.as_view(),
        name='_'.join([PREFIX, 'feature'])),
    url(r'^feature/(?P<blog_id>\d+)/(?P<page>\d+)$',
        FeatureView.as_view(), name='_'.join([PREFIX, 'feature'])),
    # tag
    url(r'^tag/(?P<tag_id>\d+)$', TagView.as_view(),
        name='_'.join([PREFIX, 'tag'])),
    url(r'^tag/(?P<tag_id>\d+)/(?P<page>\d+)$',
        TagView.as_view(), name='_'.join([PREFIX, 'tag'])),
    # list
    url(r'^list$', BlogListView.as_view(), name='_'.join([PREFIX, 'list'])),
    # taglist
    url(r'^taglist$', TagListView.as_view(),
        name='_'.join([PREFIX, 'taglist'])),
    # entry detail
    url(r'^detail/(?P<entry_id>\d+)', EntryDetailView.as_view(),
        name='_'.join([PREFIX, 'entrydetail']))
]
