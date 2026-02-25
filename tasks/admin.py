from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'category', 'due_date', 'created_at')
    list_filter = ('priority', 'status', 'category')
    search_fields = ('title', 'description')
