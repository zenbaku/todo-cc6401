from __future__ import unicode_literals

from django.db import models
from ordered_model.models import OrderedModel


class Todo(OrderedModel):
    description = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta(OrderedModel.Meta):
        pass
