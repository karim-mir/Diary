from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from diary.models import Entry, Tag

class Command(BaseCommand):
    help = 'Load demo data for diary app'

    def handle(self, *args, **options):
        # Создаем демо-пользователя
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@example.com'}
        )
        user.set_password('demo123')
        user.save()

        # Создаем теги
        tags = []
        for tag_name in ['личное', 'работа', 'идеи', 'путешествия']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        # Создаем демо-записи
        demo_entries = [
            {'title': 'Мой первый день', 'content': 'Это было прекрасно...'},
            {'title': 'Рабочие заметки', 'content': 'Нужно сделать...'},
            {'title': 'Насытить распорядок дня', 'content': 'Хочу ввести в свой распорядок дня новую привычку...'},
            {'title': 'Города, которые я хочу посетить', 'content': 'Хочу посетить Калининград, Казань, Самару...'},
        ]

        for i, entry_data in enumerate(demo_entries):
            entry = Entry.objects.create(
                title=entry_data['title'],
                content=entry_data['content'],
                author=user
            )
            entry.tags.set(tags[:4])  # Добавляем первые 4 тега
