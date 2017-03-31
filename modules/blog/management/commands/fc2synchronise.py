# -*- coding: utf-8 -*-
import urllib2
from datetime import datetime

import pytz
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from ...models import BlogFacade


def hr():
    print '-' * 24


class Command(BaseCommand):

    """RSSから取得したブログのエントリー情報をDBに保存する.

    すでに登録したものは無視される

    """

    def handle(self, *args, **options):
        blog_id = args[0]
        url = args[1]

        facade = BlogFacade()
        self.blogsynchronise(facade, blog_id, url)
        facade.create_tag_master()

    def get_entry(self, url):
        html = urllib2.urlopen(url)
#         soup = BeautifulSoup(html, "lxml")
        soup = BeautifulSoup(html)

        index = 1

        return {
            'id': url,
            'link': url,
            'title': unicode(soup.select(
                '.content .entry_header')[index].string),
            'published': self.get_published(str(soup.select(
                '.entry_footer')[index].find('li').string)[0:-1]),
            'summary': unicode(soup.select(
                '.entry_body')[index]),
            'tags': [unicode(soup.select(
                '.entry_footer')[index].find_all('li')[1].a.string)],
            'summary_detail': {}
        }

    def get_entries(self, entry_list_url):
        html = urllib2.urlopen(entry_list_url)
#         soup = BeautifulSoup(html, "lxml")
        soup = BeautifulSoup(html)

        return [self.get_entry(tag.a.get('href'))
                for tag in soup.select('.entry_header')
                if not tag.a.get('target')]

    def blogsynchronise(self, facade, blog_id, url):
        # http://and1019.blog93.fc2.com/blog-date-200901.html

        for entry in self.get_entries(url):
            facade.register(
                blog_id=blog_id,
                entry_id=entry.get('id'),
                title=entry.get('title'),
                url=entry.get('link'),
                published=entry.get('published'),
                summary=entry.get('summary'),
                summary_detail=entry.get('summary_detail', {}),
                tags=entry.get('tags', []))

            print entry.get('id')
            print entry.get('title')
            hr()

    def get_published(self, published):
        # 2013-09-30(23:46) :
        return pytz.timezone('Asia/Tokyo').localize(
            datetime.strptime(published, '%Y-%m-%d(%H:%M) :'))
