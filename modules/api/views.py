# -*- coding: utf-8 -*-
import datetime

import PyRSS2Gen
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import View

from modules.blog.models import Entry


class XMLResponseView(View):
    content_type = 'application/xml; charset=UTF-8'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return HttpResponse(context, **response_kwargs)


class RSSView(XMLResponseView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        site_domain = settings.SITE_DOMAIN
        rss = PyRSS2Gen.RSS2(
            title='itkr.net',
            link='http://{}'.format(site_domain),
            description='itkrの個人的なブログなどをまとめています',
            lastBuildDate=datetime.datetime.utcnow())
        for entry in Entry.filter_by().order_by('-published')[:5]:
            rss.items.append(PyRSS2Gen.RSSItem(
                title=entry.title,
                link='http://{}/blog/detail/{}'.format(site_domain, entry.id),
                description=entry.summary,
                author='itkr',
                pubDate=entry.published,
                categories=[tag.name for tag in entry.tags]))
        return rss.to_xml('utf-8')
