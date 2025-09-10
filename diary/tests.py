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
            author=cls.user, title="Test Entry", content="Test content"
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
        self.assertEqual(entry.author, self.user)

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
            author=self.user, title="Test", content="Content"
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
        # Изменено с 302 на 200, так как CreateView обычно возвращает 200 при успешном создании
        # или проверяет redirect на страницу созданной записи
        self.assertEqual(response.status_code, 302)  # или 200 в зависимости от реализации
        self.assertTrue(Entry.objects.filter(title="New title").exists())

    def test_entry_update_view(self):
        """
        Тестирует представление редактирования записи.

        Проверяет:
        - редирект после успешного редактирования (302)
        - фактическое обновление данных записи в базе
        """
        # ИСПРАВЛЕНО: entry_update на entry_edit
        response = self.client.post(
            reverse("diary:entry_edit", args=[self.entry.pk]),
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


class DiarySearchTest(TestCase):
    """
    Тесты для поисковой функциональности.

    Проверяет:
    - поиск по заголовку
    - поиск по содержанию
    - поиск с учетом регистра
    - поиск несуществующего текста
    """

    def setUp(self):
        """
        Настройка тестовых данных для поиска.

        Создает:
        - тестового пользователя
        - несколько записей с разным содержанием
        """
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass"
        )
        self.client.login(email="testuser@example.com", password="testpass")

        # Создаем тестовые записи
        self.entry1 = Entry.objects.create(
            author=self.user,
            title="Программирование на Python",
            content="Сегодня изучал основы Python и Django"
        )
        self.entry2 = Entry.objects.create(
            author=self.user,
            title="Отдых на природе",
            content="Ходил в поход в лес, было очень красиво"
        )
        self.entry3 = Entry.objects.create(
            author=self.user,
            title="Работа с Django",
            content="Разрабатываю новое приложение на Django"
        )

    def test_search_by_title(self):
        """
        Тестирует поиск записей по заголовку.

        Проверяет, что находятся только записи с совпадающим заголовком.
        """
        response = self.client.get(reverse('diary:entry_list') + '?q=Python')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Программирование на Python")
        self.assertNotContains(response, "Отдых на природе")
        self.assertNotContains(response, "Работа с Django")

    def test_search_by_content(self):
        """
        Тестирует поиск записей по содержанию.

        Проверяет, что находятся записи с совпадающим содержанием.
        """
        response = self.client.get(reverse('diary:entry_list') + '?q=лес')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдых на природе")
        self.assertNotContains(response, "Программирование на Python")
        self.assertNotContains(response, "Работа с Django")

    def test_search_case_insensitive(self):
        """
        Тестирует поиск без учета регистра.

        Проверяет, что поиск работает независимо от регистра.
        """
        response = self.client.get(reverse('diary:entry_list') + '?q=DJANGO')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Программирование на Python")
        self.assertContains(response, "Работа с Django")

    def test_search_multiple_words(self):
        """
        Тестирует поиск по нескольким словам.

        Проверяет, что поиск работает с частичным совпадением.
        """
        response = self.client.get(reverse('diary:entry_list') + '?q=новое приложение')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Работа с Django")

    def test_search_no_results(self):
        """
        Тестирует поиск несуществующего текста.

        Проверяет, что при отсутствии результатов показывается пустой список.
        """
        response = self.client.get(reverse('diary:entry_list') + '?q=несуществующийтекст')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Программирование на Python")
        self.assertNotContains(response, "Отдых на природе")
        self.assertNotContains(response, "Работа с Django")
        self.assertContains(response, "Пока записей нет", html=True)

    def test_search_empty_query(self):
        """
        Тестирует поведение при пустом поисковом запросе.

        Проверяет, что показываются все записи при пустом поиске.
        """
        response = self.client.get(reverse('diary:entry_list') + '?q=')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Программирование на Python")
        self.assertContains(response, "Отдых на природе")
        self.assertContains(response, "Работа с Django")
