# -*- coding: utf-8 -*-
from django.utils.functional import cached_property


class Pager(object):

    def __init__(self, cls, page_length, order_by, attrs={}):
        index = 1
        self.page_length = page_length
        self._filter = self._make_filter(cls, order_by, **attrs)
        self.count = self._get_count()
        self.data = self._get_data(index)
        self._update_information(index)

    def _make_filter(self, cls, order_by, **attrs):
        def _filter():
            return cls.objects.filter(**attrs).order_by(order_by) \
                if order_by else cls.objects.filter(**attrs)
        return _filter

    def _get_count(self):
        return self._filter().count()

    def _get_data(self, page):
        start = (page - 1) * self.page_length
        end = page * self.page_length
        return self._filter()[start:end]

    def _update_information(self, index):
        max_page = self.count / self.page_length
        if self.count % self.page_length:
            max_page += 1
        self.current_page = index
        self.prev_page = index - 1
        self.next_page = index + 1 if index < max_page else 0
        self.max_page = max_page
        self.index = index

    def page(self, index=1):
        self._update_information(index)
        self.data = self._get_data(index)
        return self

    def has_next(self):
        return self.current_page < self.max_page

    def has_previous(self):
        return 1 < self.current_page

    def has_other_pages(self):
        return self.has_next() or self.has_previous()

    def next_page_number(self):
        return self.index + 1

    def previous_page_number(self):
        return self.index - 1

    @cached_property
    def count(self):
        return self._get_count()

    @property
    def num_pages(self):
        return self.max_page

    @property
    def page_range(self):
        return [i + 1 for i in range(self.num_pages)]


class PagerMixin(object):
    """
    pager機能を追加する
    """

    @classmethod
    def get_pager(cls, page_length=20, order_by=None, attrs={}):
        return Pager(cls, page_length, order_by, attrs)
