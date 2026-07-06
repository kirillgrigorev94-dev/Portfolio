import logging
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project

logger = logging.getLogger('projects')  # <-- это ключевой момент

# Создаем словарь один раз, чтобы не дублировать код
CATEGORIES_DICT = dict(Project.CATEGORY_CHOICES)

def project_list(request):
    logger.debug("project_list: начало обработки запроса, GET=%s", request.GET)
    
    # 1. Получаем все проекты, которые НЕ в архиве (или логика по статусу)
    projects = Project.objects.exclude(status='archived').order_by('-completion_date')
    
    # 2. ФИЛЬТРАЦИЯ ПО КАТЕГОРИИ
    category = request.GET.get('category')
    if category:
        logger.info("project_list: фильтрация по категории category=%s", category)
        projects = projects.filter(category=category)
    
    # 2. Инициализируем пагинатор: 6 проектов на страницу
    paginator = Paginator(projects, 6)
    
    # 3. Получаем номер текущей страницы из GET-параметра (?page=2)
    page_number = request.GET.get('page')
    
    # 4. Получаем объект страницы (список проектов для этой страницы)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        logger.debug("project_list: page не число, берём страницу 1")
        # Если передали не число, показываем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        logger.warning("project_list: номер страницы слишком большой, показываем последнюю")
        # Если номер страницы слишком большой, показываем последнюю
        page_obj = paginator.page(paginator.num_pages)
    except Exception as e:
        logger.exception("Ошибка в project_list при обработке пагинации")
    
    logger.info(
        "project_list: отображаем страницу %s, проектов на странице: %s, всего: %s",
        page_obj.number,
        len(page_obj.object_list),
        paginator.count,
    )

    return render(request, 'projects/list.html', {
        'page_obj': page_obj,
        'page_title': 'Мои проекты',
        'current_category': category,
        # Передаем полный словарь: {'web': 'Веб-разработка', 'app': 'Мобильные приложения'...}
        'categories_dict': CATEGORIES_DICT, 
        'base_url': request.path
    })

def archive_view(request):
    logger.debug("archive_view: начало обработки запроса, GET=%s", request.GET)
    
    # 1. Получаем ТОЛЬКО архивные проекты
    projects = Project.objects.filter(status='archived').order_by('-completion_date')
    
    category = request.GET.get('category')
    if category:
        logger.info("archive_view: фильтрация архива по категории category=%s", category)
        projects = projects.filter(category=category)
    
    # 2. Та же логика пагинации
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        logger.debug("archive_view: page не число, берём страницу 1")
        page_obj = paginator.page(1)
    except EmptyPage:
        logger.warning("archive_view: номер страницы слишком большой, показываем последнюю")
        page_obj = paginator.page(paginator.num_pages)
    except Exception as e:
        logger.exception("Ошибка в project_list при обработке пагинации")
        
    logger.info(
        "archive_view: отображаем архив, страница %s, проектов: %s, всего в архиве: %s",
        page_obj.number,
        len(page_obj.object_list),
        paginator.count,
    )

    return render(request, 'projects/list.html', {
        'page_obj': page_obj,
        'page_title': 'Архив проектов',
        'current_category': category,
        # Тоже передаем словарь для архива
        'categories_dict': CATEGORIES_DICT,
        'base_url': request.path
    })