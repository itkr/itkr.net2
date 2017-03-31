# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

TEMPLATE_DIRECTORY = 'profile'


class IndexView(TemplateView):
    template_name = '/'.join([TEMPLATE_DIRECTORY, 'index.html'])

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        return {
        }
