import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели пользователя CustomUser.

    Переопределяет стандартные методы создания пользователя и суперпользователя
    для работы с email вместо username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с указанным email и паролем.

        Аргументы:
            email (str): Email адрес пользователя (обязательный)
            password (str): Пароль пользователя
            **extra_fields: Дополнительные поля модели пользователя

        Возвращает:
            CustomUser: Созданный объект пользователя

        Исключения:
            ValueError: Если email не указан
        """
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с расширенными правами.

        Аргументы:
            email (str): Email адрес суперпользователя
            password (str): Пароль суперпользователя
            **extra_fields: Дополнительные поля модели пользователя

        Возвращает:
            CustomUser: Созданный объект суперпользователя

        Исключения:
            ValueError: Если не установлены флаги is_staff или is_superuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с аутентификацией по email.

    Наследует от AbstractUser и заменяет поле username на email
    в качестве основного идентификатора пользователя.

    Атрибуты:
        username (None): Отключено стандартное поле username
        email (EmailField): Уникальный email адрес пользователя
        USERNAME_FIELD: Поле для аутентификации (email)
        REQUIRED_FIELDS: Обязательные поля при создании пользователя
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Строковое представление объекта пользователя.

        Возвращает:
            str: Email адрес пользователя
        """
        return self.email


class EmailConfirmation(models.Model):
    """
    Модель для хранения токенов подтверждения email адреса.

    Создается при регистрации нового пользователя и удаляется
    после успешного подтверждения email.

    Атрибуты:
        user (OneToOneField): Ссылка на пользователя
        token (UUIDField): Уникальный токен подтверждения
        created_at (DateTimeField): Дата и время создания токена
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подтверждение email"
        verbose_name_plural = "Подтверждения email"

    def __str__(self):
        """
        Строковое представление объекта подтверждения email.

        Возвращает:
            str: Email пользователя и дата создания
        """
        return f"Подтверждение для {self.user.email} ({self.created_at})"
