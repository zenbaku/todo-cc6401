from __future__ import unicode_literals

from django.db import models


class Todo(models.Model):
    description = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
