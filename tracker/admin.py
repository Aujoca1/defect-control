from django.contrib import admin
from .models import Project, Defect

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')  # Что показывать в списке
    search_fields = ('name',)  # Поиск по названию

@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assigned_to') # Столбцы таблицы
    list_filter = ('status', 'priority', 'project') # Фильтры справа
    search_fields = ('title', 'description') # Поиск