from django.contrib import admin
from django.urls import path, include 

# Теперь вместо нашей тестовой функции home_view, мы подключаем наше приложение
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')), # <--- Здесь мы подключаем наш tracker
]