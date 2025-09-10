from django.contrib import admin
from .models import Entry, Tag


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Entry.

    Настройки:
        list_display: Поля, отображаемые в списке записей.
        list_filter: Поля для фильтрации записей.
        search_fields: Поля для поиска записей.
    """
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'tags']
    search_fields = ['title', 'content', 'author__username']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Tag.

    Настройки:
        list_display: Поля, отображаемые в списке тегов.
        search_fields: Поля для поиска тегов.
    """
    list_display = ['name']
    search_fields = ['name']
