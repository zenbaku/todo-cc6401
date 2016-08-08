from django.contrib import admin

from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'is_completed', 'created_at')
    list_display_links = ('description',)
    date_hierarchy = 'created_at'

admin.site.register(Todo, TodoAdmin)
