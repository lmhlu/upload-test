# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

def upload_handler(instance, filename):
    return 'upload_license{}/{}'.format(instance.user.id, filename)

class UploadLicense(models.Model):
    file = models.ImageField(upload_to='upload_license/')
