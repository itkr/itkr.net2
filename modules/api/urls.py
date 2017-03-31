# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import RSSView

PREFIX = 'api'

urlpatterns = [
    url(r'^rss$', RSSView.as_view(), name=PREFIX),
]
