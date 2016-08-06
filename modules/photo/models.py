import os

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property


class Photo(models.Model):

    title = models.CharField(max_length=32, default='')
    path = models.CharField(max_length=32, null=False, blank=False)

    class Meta:
        app_label = 'photo'

    def __unicode__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.title)

    @cached_property
    def file_path(self):
        return ''.join([settings.STATIC_URL,
                        os.sep.join(['img', 'photo', self.path])])
