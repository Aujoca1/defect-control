from django.urls import path
from . import views

urlpatterns = [
    # Главная страница приложения, где будет список дефектов
    path('', views.defect_list, name='defect_list'), 
    
    # Страница для регистрации нового дефекта (для инженеров)
    path('add/', views.DefectCreateView.as_view(), name='defect_add'),
]