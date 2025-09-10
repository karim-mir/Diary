from django.conf import settings
from django.db import models


class Tag(models.Model):
    """
    Модель тега для categorizing записей дневника.

    Атрибуты:
        name (CharField): Название тега (максимум 50 символов).
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    """
    Модель записи в дневнике.
    Атрибуты:
        title (CharField): Заголовок записи.
        content (TextField): Содержание записи.
        created_at (DateTimeField): Дата и время создания записи.
        author (ForeignKey): Ссылка на пользователя-автора записи.
        tags (ManyToManyField): Теги, связанные с записью.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.title
