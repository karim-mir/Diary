from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Entry

User = get_user_model()

# Тесты для models.py
class EntryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='testuser@example.com',
            password='pass'
        )
        cls.entry = Entry.objects.create(
            user=cls.user,
            title='Test Entry',
            content='Test content'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.entry), self.entry.title)

    def test_fields_content(self):
        entry = self.entry
        self.assertEqual(entry.title, 'Test Entry')
        self.assertEqual(entry.content, 'Test content')
        self.assertEqual(entry.user, self.user)

    def test_ordering(self):
        qs = Entry.objects.all()
        self.assertEqual(list(qs), [self.entry])


# Тесты для views.py
class DiaryViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='pass'
        )
        self.client.login(email='testuser@example.com', password='pass')
        self.entry = Entry.objects.create(user=self.user, title='Test', content='Content')

    def test_entry_list_view(self):
        response = self.client.get(reverse('diary:entry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.title)
        self.assertTemplateUsed(response, 'diary/entry_list.html')

    def test_entry_detail_view(self):
        response = self.client.get(reverse('diary:entry_detail', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.content)
        self.assertTemplateUsed(response, 'diary/entry_detail.html')

    def test_entry_create_view(self):
        response = self.client.post(
            reverse('diary:entry_create'),
            {'title': 'New title', 'content': 'New content'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(title='New title').exists())

    def test_entry_update_view(self):
        response = self.client.post(
            reverse('diary:entry_edit', args=[self.entry.pk]),
            {'title': 'Updated title', 'content': 'Updated content'}
        )
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Updated title')

    def test_entry_delete_view(self):
        response = self.client.post(reverse('diary:entry_delete', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())
