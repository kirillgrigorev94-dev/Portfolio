from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'completion_date', 'created_at', 'category']
    list_filter = ['status', 'completion_date', 'category']
    search_fields = ['title', 'description', 'technologies']
    date_hierarchy = 'completion_date'