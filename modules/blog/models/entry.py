# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from django.db import models
from django.utils import html
from django.utils.functional import cached_property

from modules.bases.models import ModelWrapper
from modules.tools.djangopager import PagerMixin
from modules.tools.html import htmlentity2unicode

from .blog import Blog


class TagStyle(object):
    fixture = [
        {'name': 'post-category-js', 'number': 10, },
        {'name': 'post-category-yui', 'number': 7, },
        {'name': 'post-category-pure', 'number': 5, },
        {'name': 'post-category-design', 'number': 2, },
    ]

    @classmethod
    def get(cls, count):
        for data in sorted(cls.fixture,
                           key=lambda x: x['number'], reverse=True):
            if count >= data['number']:
                return data['name']


class Tag(ModelWrapper):

    name = models.CharField(unique=True, max_length=255, default='')
    count = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        app_label = 'blog'

    @classmethod
    def register(cls, name):
        cls.objects.create(name=name)

    @cached_property
    def style(self):
        return TagStyle.get(self.count)


class EntryTag(ModelWrapper):

    name = models.CharField(max_length=255, default='')
    entry_id = models.CharField(max_length=255, null=False)

    class Meta:
        app_label = 'blog'
        unique_together = ('entry_id', 'name', )

    @classmethod
    def register(cls, entry_id, name):
        cls.objects.create(entry_id=entry_id, name=name)

    @cached_property
    def entry(self):
        return Entry.objects.get(entry_id=self.entry_id)

    @cached_property
    def tag(self):
        return Tag.objects.get(name=self.name)


class Entry(ModelWrapper, PagerMixin):

    blog_id = models.PositiveIntegerField(null=False, default=0)
    title = models.CharField(max_length=255, default='')
    entry_id = models.CharField(max_length=255, unique=True, default='')
    url = models.CharField(max_length=255, unique=True, default='')  # link
    published = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(default='')
    summary_detail = models.TextField(default='')

    class Meta:
        app_label = 'blog'

    @classmethod
    def register(cls, blog_id, entry_id, title, url,
                 published, summary, summary_detail):

        return cls.objects.create(
            blog_id=blog_id,
            entry_id=entry_id,
            title=title,
            url=url,
            published=published,
            summary=summary,
            summary_detail=summary_detail)

    @cached_property
    def blog(self):
        return Blog.get(self.blog_id)

    @cached_property
    def tags(self):
        try:
            return [entry_tag.tag for entry_tag
                    in list(EntryTag.filter_by(entry_id=self.entry_id))]
        except EntryTag.DoesNotExist:
            return []

    @cached_property
    def descliption(self):
        return htmlentity2unicode(html.strip_tags(self.summary))[:250]

    @cached_property
    def _summary_soup(self):
        #         return BeautifulSoup(self.summary, "lxml")
        return BeautifulSoup(self.summary, 'html.parser')

    @cached_property
    def escaped_summary(self):
        soup = self._summary_soup

        # TODO: もう少し汎用化
        # hatena
        for hatena_keyword in soup.find_all(class_='keyword'):
            hatena_keyword.unwrap()

        # fc2
        for fc2_infeed in soup.find_all(class_=re.compile('^fc2_infeed')):
            fc2_infeed.extract()

        for a_tag in soup.find_all('a'):
            a_tag['target'] = '_new'

        return soup.prettify()

    @cached_property
    def img(self):
        img_tag = self._summary_soup.find('img')
        return img_tag.get('src') if img_tag else None

    @cached_property
    def img2(self):
        img_tags = self._summary_soup.find_all('img')
        if len(img_tags) >= 2:
            return img_tags[1].get('src')
