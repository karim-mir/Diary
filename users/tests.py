import uuid

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from users.forms import CustomUserRegistrationForm

from .models import EmailConfirmation

User = get_user_model()


# Тесты для forms.py
class CustomUserRegistrationFormTest(TestCase):
    """Тесты для формы регистрации пользователя CustomUserRegistrationForm."""

    def test_form_valid_data(self):
        """Тест корректной валидации формы с правильными данными."""
        form_data = {
            "email": "testuser@example.com",
            "password1": "strong_password123",
            "password2": "strong_password123",
        }
        form = CustomUserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("strong_password123"))

    def test_form_password_mismatch(self):
        """Тест валидации формы при несовпадении паролей."""
        form_data = {
            "email": "testuser@example.com",
            "password1": "password1",
            "password2": "password2",
        }
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_missing_email(self):
        """Тест валидации формы при отсутствии email."""
        form_data = {
            "email": "",
            "password1": "strong_password123",
            "password2": "strong_password123",
        }
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


# Тесты для models.py
class CustomUserModelTest(TestCase):
    """Тесты для модели пользователя CustomUser."""

    def test_create_user(self):
        """Тест создания обычного пользователя."""
        user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Тест создания суперпользователя."""
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_user_no_email(self):
        """Тест создания пользователя без email (должен вызывать исключение)."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="pass")


class EmailConfirmationModelTest(TestCase):
    """Тесты для модели подтверждения email."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.user = User.objects.create_user(
            email="user2@example.com", password="pass123"
        )

    def test_email_confirmation_creation(self):
        """Тест создания объекта подтверждения email."""
        confirmation = EmailConfirmation.objects.create(user=self.user)
        self.assertEqual(confirmation.user, self.user)
        self.assertIsInstance(confirmation.token, uuid.UUID)
        self.assertIsNotNone(confirmation.created_at)

    def test_email_confirmation_str(self):
        """Тест строкового представления объекта подтверждения email."""
        confirmation = EmailConfirmation.objects.create(user=self.user)


# Тесты для views.py
class UsersViewsTest(TestCase):
    """Тесты для views модуля users."""

    def test_register_view_get(self):
        """Тест GET-запроса к странице регистрации."""
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_view_post_valid(self):
        """Тест POST-запроса с валидными данными регистрации."""
        data = {
            "email": "testuser@example.com",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration_pending.html")
        self.assertFalse(User.objects.get(email="testuser@example.com").is_active)

        # Проверка, что письмо отправлено
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Подтверждение регистрации", mail.outbox[0].subject)
        self.assertIn("testuser@example.com", mail.outbox[0].to)

    def test_confirm_email_valid_token(self):
        """Тест подтверждения email с валидным токеном."""
        user = User.objects.create_user(
            email="testuser2@example.com", password="pass", is_active=False
        )
        from users.models import EmailConfirmation

        confirmation = EmailConfirmation.objects.create(user=user)

        url = reverse("users:confirm_email", args=[str(confirmation.token)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_success.html")

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertFalse(EmailConfirmation.objects.filter(user=user).exists())

    def test_confirm_email_invalid_token(self):
        """Тест подтверждения email с невалидным токеном."""
        url = reverse(
            "users:confirm_email", args=["00000000-0000-0000-0000-000000000000"]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_invalid.html")

    def test_login_view_get(self):
        """Тест GET-запроса к странице входа."""
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post_valid(self):
        """Тест POST-запроса с валидными данными входа."""
        user = User.objects.create_user(email="loginuser@example.com", password="pass")
        data = {
            "username": user.email,  # форма по умолчанию использует поле username для логина, здесь email
            "password": "pass",
        }
        response = self.client.post(reverse("users:login"), data)
        self.assertRedirects(response, reverse("diary:entry_list"))

    def test_logout_view(self):
        """Тест выхода из системы."""
        user = User.objects.create_user(email="logoutuser@example.com", password="pass")
        self.client.login(email=user.email, password="pass")
        response = self.client.get(reverse("users:logout"))
        self.assertRedirects(response, reverse("users:login"))

    def test_home_view(self):
        """Тест домашней страницы пользователя."""
        response = self.client.get(reverse("users:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/home.html")
