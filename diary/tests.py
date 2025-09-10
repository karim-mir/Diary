from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry

User = get_user_model()


class EntryModelTest(TestCase):
    """
    Тесты для модели Entry.

    Проверяет:
    - строковое представление модели
    - содержание полей модели
    - правильность ordering
    """

    @classmethod
    def setUpTestData(cls):
        """
        Настройка тестовых данных для всех тестов класса.

        Создает:
        - тестового пользователя
        - тестовую запись дневника
        """
        cls.user = User.objects.create_user(
            email="testuser@example.com", password="pass"
        )
        cls.entry = Entry.objects.create(
            author=cls.user, title="Test Entry", content="Test content"  # ← Исправлено user на author
        )

    def test_string_representation(self):
        """
        Тестирует строковое представление модели Entry.

        Проверяет, что __str__ возвращает заголовок записи.
        """
        self.assertEqual(str(self.entry), self.entry.title)

    def test_fields_content(self):
        """
        Тестирует содержание полей модели Entry.

        Проверяет корректность сохранения:
        - заголовка
        - содержания
        - автора записи
        """
        entry = self.entry
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)  # ← Исправлено user на author

    def test_ordering(self):
        """
        Тестирует ordering в мета-классе модели Entry.

        Проверяет, что записи упорядочены по дате создания (сначала новые).
        """
        qs = Entry.objects.all()
        self.assertEqual(list(qs), [self.entry])


class DiaryViewsTest(TestCase):
    """
    Тесты для views приложения Diary.

    Проверяет работу всех основных представлений:
    - список записей
    - детальный просмотр записи
    - создание записи
    - редактирование записи
    - удаление записи
    """

    def setUp(self):
        """
        Настройка тестовых данных для каждого теста.

        Создает:
        - тестового пользователя
        - выполняет вход
        - создает тестовую запись
        """
        self.user = User.objects.create_user(
            email="testuser@example.com", password="pass"
        )
        self.client.login(email="testuser@example.com", password="pass")
        self.entry = Entry.objects.create(
            author=self.user, title="Test", content="Content"  # ← Исправлено user на author
        )

    def test_entry_list_view(self):
        """
        Тестирует представление списка записей.

        Проверяет:
        - статус код ответа (200)
        - наличие заголовка записи в ответе
        - использование правильного шаблона
        """
        response = self.client.get(reverse("diary:entry_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.title)
        self.assertTemplateUsed(response, "diary/entry_list.html")

    def test_entry_detail_view(self):
        """
        Тестирует представление детальной информации о записи.

        Проверяет:
        - статус код ответа (200)
        - наличие содержания записи в ответе
        - использование правильного шаблона
        """
        response = self.client.get(reverse("diary:entry_detail", args=[self.entry.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.content)
        self.assertTemplateUsed(response, "diary/entry_detail.html")

    def test_entry_create_view(self):
        """
        Тестирует представление создания новой записи.

        Проверяет:
        - редирект после успешного создания (302)
        - фактическое создание записи в базе данных
        """
        response = self.client.post(
            reverse("diary:entry_create"),
            {"title": "New title", "content": "New content"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(title="New title").exists())

    def test_entry_update_view(self):
        """
        Тестирует представление редактирования записи.

        Проверяет:
        - редирект после успешного редактирования (302)
        - фактическое обновление данных записи в базе
        """
        response = self.client.post(
            reverse("diary:entry_update", args=[self.entry.pk]),  # ← Исправлено entry_edit на entry_update
            {"title": "Updated title", "content": "Updated content"},
        )
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Updated title")

    def test_entry_delete_view(self):
        """
        Тестирует представление удаления записи.

        Проверяет:
        - редирект после успешного удаления (302)
        - фактическое удаление записи из базы данных
        """
        response = self.client.post(reverse("diary:entry_delete", args=[self.entry.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())
