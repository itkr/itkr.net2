# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.main import IndexView

PREFIX = 'profile'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name=PREFIX)
]
