# -*- coding: utf-8 -*-
from django.db import models


class ModelWrapper(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def get(cls, pk):
        return cls.objects.get(pk=pk)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.objects.get(**kwargs)

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.objects.filter(**kwargs)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_for_update(cls, **kwargs):
        return cls.objects.select_for_update().get(**kwargs)

    @classmethod
    def register(cls, **kwargs):
        return cls.objects.create(**kwargs)
