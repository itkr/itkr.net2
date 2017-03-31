# -*- coding: utf-8 -*-
from django.contrib import admin


class BlogAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'url')
