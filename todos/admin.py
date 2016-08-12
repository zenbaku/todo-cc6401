from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import Todo


class TodoAdmin(OrderedModelAdmin):
    list_display = (
        'id', 'description', 'is_completed', 'created_at', 'move_up_down_links'
    )
    list_display_links = ('description',)
    date_hierarchy = 'created_at'

admin.site.register(Todo, TodoAdmin)
