# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import TimeStampedModel
from .utils.auth import hash_api_key


class ClientManager(models.Manager):
    def create(self, *args, **kwargs):
        kwargs['api_key'] = hash_api_key(kwargs['api_key'])
        return super().create(*args, **kwargs)


class Client(TimeStampedModel):
    name = models.CharField(max_length=20)
    api_key = models.CharField(max_length=255)

    objects = ClientManager()
