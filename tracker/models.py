from django.db import models
from django.contrib.auth.models import User

# Модель Объекта/Проекта
class Project(models.Model):
    name = models.CharField("Название объекта", max_length=200)
    description = models.TextField("Описание", blank=True)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Строительный объект"
        verbose_name_plural = "Строительные объекты"

# Модель Дефекта
class Defect(models.Model):
    # ПЕРЕМЕННЫЕ ПЕРЕНЕСЕНЫ ВНУТРЬ КЛАССА
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('verify', 'На проверке'),
        ('closed', 'Закрыта'),
        ('canceled', 'Отменена'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
    ]

    title = models.CharField("Заголовок дефекта", max_length=200)
    description = models.TextField("Описание проблемы")
    image = models.ImageField("Фото дефекта", upload_to='defects/', blank=True, null=True) 
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new') # Использование переменной внутри класса
    priority = models.IntegerField("Приоритет", choices=PRIORITY_CHOICES, default=2)
    
    # Связи
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Объект")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_defects', verbose_name="Исполнитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Дефект"
        verbose_name_plural = "Дефекты"