from django.urls import path
from . import views

urlpatterns = [
    path('', views.defect_list, name='defect_list'), 
    path('add/', views.DefectCreateView.as_view(), name='defect_add'),
    path('export/', views.export_defects_csv, name='export_csv'), 
]