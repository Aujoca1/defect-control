from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Defect, Project
from .filters import DefectFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse 
import csv 

# 1. Форма для создания дефекта (Create)
class DefectCreateView(LoginRequiredMixin, CreateView):
    model = Defect 
    # Поля, которые Инженер заполняет по ТЗ: заголовок, описание, приоритет, вложения и т.д.
    fields = ['project', 'title', 'description', 'priority', 'image', 'assigned_to', 'status'] 
    template_name = 'tracker/defect_form.html' 
    success_url = reverse_lazy('defect_list') 
    
    def form_valid(self, form):
        # Назначаем исполнителем текущего авторизованного пользователя
        form.instance.assigned_to = self.request.user 
        return super().form_valid(form)

# 2. Список дефектов (Read and Filter)
class DefectListView(LoginRequiredMixin, ListView):
    model = Defect
    template_name = 'tracker/defect_list.html'
    context_object_name = 'defects'
    
    def get_queryset(self):
        # Получаем все дефекты, отсортированные по дате (требование ТЗ: Сортировка)
        return Defect.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Применяем фильтр (требование ТЗ: Поиск и фильтрация)
        f = DefectFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = f
        context['defects'] = f.qs
        return context

# Передаем классовое представление в urls.py
defect_list = DefectListView.as_view() 

# 3. Функция для экспорта в CSV (Reports) (требование ТЗ: Экспорт отчётности в CSV/Excel)
def export_defects_csv(request):
    # Применяем фильтр, чтобы экспортировались только те данные, которые видит пользователь
    f = DefectFilter(request.GET, queryset=Defect.objects.all())
    defects = f.qs 
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="defects_report.csv"'},
    )

    writer = csv.writer(response)
    
    # Записываем заголовки
    writer.writerow(['ID', 'Заголовок', 'Объект', 'Приоритет', 'Статус', 'Исполнитель', 'Дата создания'])
    
    # Записываем данные
    for defect in defects:
        writer.writerow([
            defect.id,
            defect.title,
            defect.project.name if defect.project else '',
            defect.get_priority_display(),
            defect.get_status_display(),
            defect.assigned_to.username if defect.assigned_to else 'Не назначен',
            defect.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return response