# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from modules.photo.models import Photo


class IndexView(TemplateView):
    template_name = 'root/index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'photos': Photo.objects.all()[0:4],
        })


class TestView(TemplateView):
    template_name = 'root/test.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
