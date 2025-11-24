import django_filters
from .models import Defect, Project

class DefectFilter(django_filters.FilterSet):
    # Фильтр по названию дефекта (поиск)
    title = django_filters.CharFilter(lookup_expr='icontains', label='Поиск по заголовку')
    
    # Фильтр по статусу (выпадающий список)
    status = django_filters.ChoiceFilter(choices=Defect.STATUS_CHOICES, label='Статус')
    
    # Фильтр по приоритету
    priority = django_filters.ChoiceFilter(choices=Defect.PRIORITY_CHOICES, label='Приоритет')

    # Фильтр по объекту (выпадающий список проектов)
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all(), label='Объект')

    class Meta:
        model = Defect
        # Все поля, которые можно фильтровать/искать
        fields = ['title', 'status', 'priority', 'project']