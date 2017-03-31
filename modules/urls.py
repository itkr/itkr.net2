# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('modules.blog.urls')),
    # url(r'^blog', include('modules.blog.urls')),
    url(r'^profile', include('modules.profile.urls')),
    # api
    url(r'^api/', include('modules.api.urls')),
]
