from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Defect, Project
from django.contrib.auth.mixins import LoginRequiredMixin # Защита от неавторизованных

# 1. Форма для создания дефекта (требование ТЗ: Инженер регистрирует дефект)
class DefectCreateView(LoginRequiredMixin, CreateView):
    # Указываем, какую модель мы создаем
    model = Defect 
    
    # Какие поля из модели должны быть в форме
    fields = ['project', 'title', 'description', 'priority', 'image', 'assigned_to', 'status'] 
    
    # Файл шаблона (создадим его в следующем шаге)
    template_name = 'tracker/defect_form.html' 
    
    # Куда перенаправить после успешного сохранения
    success_url = reverse_lazy('defect_list') 
    
    # Автоматически заполняем поле создателя
    def form_valid(self, form):
        # Присваиваем исполнителю текущего авторизованного пользователя
        form.instance.assigned_to = self.request.user 
        return super().form_valid(form)

# 2. Список дефектов (главная страница)
def defect_list(request):
    # Получаем все дефекты
    defects = Defect.objects.all().order_by('-created_at') 
    
    # Передаем их в шаблон
    return render(request, 'tracker/defect_list.html', {'defects': defects})