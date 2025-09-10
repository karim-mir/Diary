# management/commands/create_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from diary.models import Entry, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test data for diary application'

    def handle(self, *args, **options):
        # Создать тестового пользователя
        user, created = User.objects.get_or_create(
            email='testuser@example.com'
        )

        if created:
            # Установить пароль ПРАВИЛЬНЫМ способом
            user.set_password('testpassword123')
            user.save()
            self.stdout.write(f'Created user: {user.email}')
        else:
            # Обновить пароль если пользователь уже существует
            user.set_password('testpassword123')
            user.save()
            self.stdout.write(f'Updated password for user: {user.email}')

        # Создать теги
        tags_data = ['Python', 'Django', 'Отдых', 'Программирование']
        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Создать тестовые записи С ТЕГАМИ
        entries_data = [
            {
                'title': 'Программирование на Python',
                'content': 'Сегодня изучал основы Python и Django',
                'tags': [tags['Python'], tags['Программирование']]
            },
            {
                'title': 'Отдых на природе',
                'content': 'Ходил в поход в лес, было очень красиво',
                'tags': [tags['Отдых']]
            },
            {
                'title': 'Работа с Django',
                'content': 'Разрабатываю новое приложение на Django',
                'tags': [tags['Django'], tags['Программирование']]
            }
        ]

        for entry_data in entries_data:
            # Извлекаем теги из данных записи
            entry_tags = entry_data.pop('tags', [])

            entry, created = Entry.objects.get_or_create(
                author=user,
                title=entry_data['title'],
                defaults=entry_data
            )

            if created:
                # Добавляем теги к созданной записи
                entry.tags.set(entry_tags)
                self.stdout.write(f'Created entry: {entry.title} with tags: {[t.name for t in entry_tags]}')
            else:
                # Обновляем теги для существующей записи
                entry.tags.set(entry_tags)
                self.stdout.write(f'Updated tags for entry: {entry.title}')

        self.stdout.write(
            self.style.SUCCESS('Test data created successfully!')
        )