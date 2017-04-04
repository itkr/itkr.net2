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

    def get_entry(self, entry_url):
        html = urllib2.urlopen(entry_url)
#         soup = BeautifulSoup(html, "lxml")
        soup = BeautifulSoup(html, 'html.parser')

        entity_id_base = soup.find('article',
                                   class_='autopagerize_page_element').get('data-uuid')
        entity_id = ''.join(['hatenablog://entry/', unicode(entity_id_base)])

        return {
            'title': unicode(soup.find('a',
                                       class_='entry-title-link').string),
            'link': unicode(soup.find('a',
                                      class_='entry-title-link').get('href')),
            'summary': unicode(soup.find('div',
                                         class_='entry-content')),
            'published': unicode(soup.find('time',
                                           class_='updated').get('datetime')),
            'tags': [article.get('content') for article in
                     soup.find_all(attrs={'property': 'article:tag'})],
            'id': entity_id,
            'summary_detail': {}
        }

    def get_entries(self, entry_list_url):
        html = urllib2.urlopen(entry_list_url)
#         soup = BeautifulSoup(html, "lxml")
        soup = BeautifulSoup(html, 'html.parser')

        return [self.get_entry(tag.get('href'))
                for tag in soup.select('.hatena-star-permalink')]

    def blogsynchronise(self, facade, blog_id, url):
        #url = "http://58.hatenablog.com/archive/2014?page=2"

        for entry in self.get_entries(url):
            facade.register(
                blog_id=blog_id,
                entry_id=entry.get('id'),
                title=entry.get('title'),
                url=entry.get('link'),
                published=self.get_published(entry),
                summary=entry.get('summary'),
                summary_detail=entry.get('summary_detail', {}),
                tags=entry.get('tags', []))
            print entry.get('id')
            print entry.get('title')
            hr()

    def get_published(self, entry):
        published = entry.get('published') or entry.get('updated')
        if published:
            return pytz.timezone('Asia/Tokyo').localize(
                datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ'))
