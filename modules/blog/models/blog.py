# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.utils.functional import cached_property

from modules.bases.models import ModelWrapper
from modules.tools.djangopager import PagerMixin

from .admin import BlogAdmin


class Blog(ModelWrapper, PagerMixin):

    title = models.CharField(max_length=30, default='')
    url = models.CharField(max_length=255, default='')
    link = models.CharField(max_length=255, default='')
    description = models.TextField(default='', null=True)

    class Meta:
        app_label = 'blog'

    @cached_property
    def entries(self):
        from .entry import Entry
        return Entry.filter_by(blog_id=self.id).order_by('-published')[:3]


admin.site.register(Blog, BlogAdmin)
