# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import TemplateView

from .models import Blog, Entry, EntryTag, Tag

TEMPLATE_DIRECTORY = 'blog'


class IndexView(TemplateView):

    """ブログのエントリー一覧."""

    template_name = '/'.join([TEMPLATE_DIRECTORY, 'index.html'])
    page_length = 10

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_pagenator_link(self, **kwargs):
        return reverse('blog')

    def get_pagenator(self, **kwargs):
        page = int(kwargs.get('page', 1))
        return Entry.get_pager(
            page_length=self.page_length, order_by='-published').page(page)

    def get_context_data(self, **kwargs):
        paginator = self.get_pagenator(**kwargs)
        return {
            'paginator': self.format_paginator(paginator),
            'entries': paginator.data,
            'paginator_link': self.get_pagenator_link(**kwargs),
            'subtitle': 'Blog',
        }

    def format_paginator(self, paginator):
        view_length = min(7, paginator.max_page)
        if paginator.current_page <= 3:
            view_list = [i + 1 for i in
                         range(view_length)]
        elif paginator.current_page >= paginator.max_page - (view_length / 2):
            view_list = [i + 1 for i in
                         range(paginator.max_page - view_length, paginator.max_page)]
        else:
            view_list = [i + 1 for i in
                         range(paginator.current_page - (view_length - view_length / 2),
                               paginator.current_page + (view_length / 2))]
        return {
            'list': view_list,
            'current_page': paginator.current_page,
            'prev_page': paginator.prev_page,
            'next_page': paginator.next_page,
            'has_next': paginator.has_next(),
            'has_prev': paginator.has_previous(),
        }


class FeatureView(IndexView):

    """ブログごとのエントリー."""

    def get_context_data(self, **kwargs):
        try:
            context = super(FeatureView, self).get_context_data(**kwargs)
            if not kwargs.get('page'):
                blog = Blog.get(kwargs['blog_id'])
                context.update({
                    'blog': blog,
                    'subtitle': blog.title,
                })
        except Blog.DoesNotExist:
            raise Http404
        return context

    def get_pagenator_link(self, **kwargs):
        return reverse('blog_feature', args=[kwargs['blog_id']])

    def get_pagenator(self, **kwargs):
        page = int(kwargs.get('page', 1))
        blog_id = int(kwargs.get('blog_id'))
        return Entry.get_pager(
            page_length=self.page_length, order_by='-published',
            attrs={'blog_id': blog_id}).page(page)


class TagView(IndexView):

    """タグごとのエントリー."""

    def get_context_data(self, **kwargs):
        try:
            context = super(TagView, self).get_context_data(**kwargs)
            context.update({
                'subtitle': Tag.get_by(id=int(kwargs.get('tag_id'))).name})
        except Tag.DoesNotExist:
            raise Http404
        return context

    def get_pagenator_link(self, **kwargs):
        return reverse('blog_tag', args=[kwargs['tag_id']])

    def get_pagenator(self, **kwargs):
        page = int(kwargs.get('page', 1))
        tag_id = int(kwargs.get('tag_id'))
        tag = Tag.get_by(id=tag_id)
        entry_tags = EntryTag.filter_by(name=tag.name)

        return Entry.get_pager(
            page_length=self.page_length, order_by='-published',
            attrs={'entry_id__in': [entry_tag.entry_id
                                    for entry_tag in entry_tags]}).page(page)


class BlogListView(TemplateView):

    """ブログ一覧."""

    template_name = '/'.join([TEMPLATE_DIRECTORY, 'bloglist.html'])

    def get_context_data(self, **kwargs):
        return {
            'blogs': Blog.get_all(),
        }


class TagListView(TemplateView):

    """タグ一覧."""

    template_name = '/'.join([TEMPLATE_DIRECTORY, 'taglist.html'])

    def get_context_data(self, **kwargs):
        return {
            'tags': sorted(
                Tag.get_all(), key=lambda x: x.count, reverse=True),
        }


class EntryDetailView(TemplateView):

    """エントリー詳細."""

    template_name = '/'.join([TEMPLATE_DIRECTORY, 'entrydetail.html'])

    def get_context_data(self, **kwargs):
        try:
            return {'entry': Entry.get(kwargs['entry_id'])}
        except Entry.DoesNotExist:
            raise Http404
