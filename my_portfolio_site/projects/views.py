from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.filter(status='completed').select_related()
    return render(request, 'projects/list.html', {'projects': projects})

def archive_view(request):
    # Архив: показываем ТОЛЬКО архивные проекты
    projects = Project.objects.filter(status='archived').select_related()
    return render(request, 'projects/list.html', {'projects': projects})