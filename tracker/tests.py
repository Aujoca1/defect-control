from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project, Defect
from datetime import date # <-- Убедись, что этот импорт есть!


class ProjectModelTest(TestCase):
    """Тестирование модели Строительного Объекта (Project)"""

    def test_project_creation(self):
        """Проверка, что объект Project создается корректно"""
        # Передаем явные объекты date(), а не строки
        project = Project.objects.create(
            name="Тестовый Проект №1",
            description="Описание тестового проекта.",
            start_date=date(2025, 1, 1), # ИСПРАВЛЕНО
            end_date=date(2025, 12, 31)  # ИСПРАВЛЕНО
        )
        # Проверяем, что ID объекта назначен (то есть, он сохранился в БД)
        self.assertTrue(project.pk is not None)
        # Проверяем, что название корректно отображается
        self.assertEqual(str(project), "Тестовый Проект №1")
        # Проверка сравнения объектов date()
        self.assertEqual(project.start_date, date(2025, 1, 1)) 


# Успех: 1 юнит-тест пройден

class DefectModelTest(TestCase):
    """Тестирование модели Дефекта (Defect)"""

    def setUp(self):
        # Создание тестового пользователя (Исполнителя)
        self.user = User.objects.create_user(
            username='test_engineer',
            password='password123'
        )
        # Создание тестового проекта
        self.project = Project.objects.create(
            name="Объект для Дефекта",
            start_date="2025-01-01"
        )

    def test_defect_creation_and_status(self):
        """Проверка создания дефекта и правильного отображения статуса"""
        defect = Defect.objects.create(
            project=self.project,
            assigned_to=self.user,
            title="Проблема с окном",
            description="Трещина в стеклопакете",
            priority=3, # Высокий приоритет
            status='new' # Статус "Новая"
        )
        # Проверяем, что дефект успешно создан
        self.assertTrue(defect.pk is not None)
        # Проверяем, что дефект привязан к нужному исполнителю
        self.assertEqual(defect.assigned_to.username, 'test_engineer')
        # Проверяем, что отображение статуса работает (Требование ТЗ: Управление статусами)
        self.assertEqual(defect.get_status_display(), 'Новая')
        # Проверяем, что приоритет корректный
        self.assertEqual(defect.get_priority_display(), 'Высокий')

# Успех: 2 юнит-теста пройдены (внутри двух классов)

from django.test import Client
from django.urls import reverse

class DefectFormTest(TestCase):
    """Тестирование форм и URL-маршрутов"""

    def setUp(self):
        self.client = Client()
        # Создание тестовых данных
        self.project = Project.objects.create(name="Тестовый Объект", start_date="2025-01-01")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.login_url = reverse('admin:index') # Используем url админки для логина в тесте

    def test_defect_create_view_auth(self):
        """Тест на успешное создание дефекта авторизованным пользователем (Интеграционный сценарий 1)"""
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('defect_add'), {
            'project': self.project.id,
            'title': 'Новый дефект через форму',
            'description': 'Описание дефекта для проверки формы.',
            'priority': 1, # Низкий
            'status': 'new',
            'assigned_to': self.user.id,
        })
        
        # Проверяем, что перенаправление после создания прошло успешно (статус 302)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что дефект действительно создан в базе
        self.assertTrue(Defect.objects.filter(title='Новый дефект через форму').exists())

# Успех: 3 юнит-теста

class DefectFilterTest(TestCase):
    """Тестирование механизма фильтрации"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='filteruser', password='password123')
        self.client.login(username='filteruser', password='password123')
        
        self.project_a = Project.objects.create(name="Проект А", start_date="2025-01-01")
        self.project_b = Project.objects.create(name="Проект Б", start_date="2025-01-01")
        
        # Создаем 3 тестовых дефекта
        Defect.objects.create(project=self.project_a, assigned_to=self.user, title="Красный дефект", status='new', priority=3)
        Defect.objects.create(project=self.project_b, assigned_to=self.user, title="Синий дефект", status='in_progress', priority=1)
        Defect.objects.create(project=self.project_b, assigned_to=self.user, title="Желтый дефект", status='in_progress', priority=2)

    def test_filter_by_status(self):
        """Тест №4: Проверка фильтрации по статусу"""
        # Фильтруем по статусу 'В работе' (in_progress)
        response = self.client.get(reverse('defect_list'), {'status': 'in_progress'})
        
        # Ожидаем, что в списке будет 2 дефекта
        self.assertEqual(len(response.context['defects']), 2) 

    def test_filter_by_priority(self):
        """Тест №5: Проверка фильтрации по приоритету"""
        # Фильтруем по приоритету 3 (Высокий)
        response = self.client.get(reverse('defect_list'), {'priority': 3})
        
        # Ожидаем, что в списке будет 1 дефект ('Красный дефект')
        self.assertEqual(len(response.context['defects']), 1)
        # Проверяем, что это именно тот дефект
        self.assertContains(response, 'Красный дефект') 

# Успех: 5 юнит-тестов