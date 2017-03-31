# -*- coding: utf-8 -*-
from datetime import datetime

import feedparser
import pytz
from django.core.management.base import BaseCommand

from ...models import Blog, BlogFacade


def hr():
    print '-' * 24


class Command(BaseCommand):

    """RSSから取得したブログのエントリー情報をDBに保存する.

    すでに登録したものは無視される

    """

    def handle(self, *args, **options):
        facade = BlogFacade()
        self.blogsynchronise(facade)
        facade.create_tag_master()

    def blogsynchronise(self, facade):
        hr()

        for blog in Blog.get_all():
            feed = feedparser.parse(blog.url)

            count = 0
            for entry in feed.get('entries'):
                if facade.register(
                        blog_id=blog.id,
                        entry_id=entry.get('id'),
                        title=entry.get('title'),
                        url=entry.get('link'),
                        published=self.get_published(entry),
                        summary=entry.get('summary'),
                        summary_detail=entry.get('summary_detail', {}),
                        tags=entry.get('tags', [])):
                    count += 1

            print blog.title.encode('utf_8')
            print count, 'entry(entries) updated.'
            hr()

    def get_published(self, entry):
        published = entry.get('published_parsed') \
            or entry.get('updated_parsed')
        if published:
            return pytz.timezone('Asia/Tokyo').localize(
                datetime(*published[:6]))
