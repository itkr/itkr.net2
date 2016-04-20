from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'root/index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class TestView(TemplateView):
    template_name = 'root/test.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
