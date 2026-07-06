from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project

def project_list(request):
    # 1. Получаем все проекты, которые НЕ в архиве (или логика по статусу)
    projects = Project.objects.exclude(status='archived').order_by('-completion_date')
    
    # 2. Инициализируем пагинатор: 6 проектов на страницу
    paginator = Paginator(projects, 6)
    
    # 3. Получаем номер текущей страницы из GET-параметра (?page=2)
    page_number = request.GET.get('page')
    
    # 4. Получаем объект страницы (список проектов для этой страницы)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если передали не число, показываем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если номер страницы слишком большой, показываем последнюю
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'projects/list.html', {
        'page_obj': page_obj,
        'page_title': 'Мои проекты'
    })

def archive_view(request):
    # 1. Получаем ТОЛЬКО архивные проекты
    projects = Project.objects.filter(status='archived').order_by('-completion_date')
    
    # 2. Та же логика пагинации
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'projects/list.html', {
        'page_obj': page_obj,
        'page_title': 'Архив проектов'
    })