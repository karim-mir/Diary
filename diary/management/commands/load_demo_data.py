from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from diary.models import Entry, Tag


class Command(BaseCommand):
    """
    Кастомная команда для загрузки демо-данных в приложение Diary.

    Создает:
    - Демо-пользователя (email: demo@example.com, password: demo123)
    - Набор тегов для categorizing записей
    - Несколько демо-записей с связанными тегами

    Использование: python manage.py load_demo_data
    """
    help = 'Загружает демо-данные для приложения Diary'

    def handle(self, *args, **options):
        """
        Основной метод выполнения команды.

        Создает демо-пользователя, теги и записи для тестирования функционала.
        """
        # Получаем модель пользователя
        User = get_user_model()

        # Создаем демо-пользователя (используем email вместо username)
        user, created = User.objects.get_or_create(
            email='demo@example.com',  # ← ТОЛЬКО email, без username!
            defaults={
                'first_name': 'Демо',
                'last_name': 'Пользователь'
            }
        )

        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS('✅ Создан демо-пользователь: demo@example.com/demo123')
            )
        else:
            # Если пользователь уже существует, обновляем пароль
            user.set_password('demo123')
            user.save()
            self.stdout.write('ℹ️ Демо-пользователь уже существовал, пароль обновлен')

        # Создаем теги
        tags = []
        for tag_name in ['личное', 'работа', 'идеи', 'путешествия']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'✅ Создан тег: {tag_name}')
            else:
                self.stdout.write(f'ℹ️ Тег уже существует: {tag_name}')

        # Создаем демо-записи
        demo_entries = [
            {
                'title': 'Мой первый день',
                'content': 'Это было прекрасное утро. Я решил начать вести дневник чтобы сохранять свои мысли и воспоминания.',
                'tags': ['личное', 'путешествия']
            },
            {
                'title': 'Рабочие заметки',
                'content': 'Нужно закончить проект по Django, подготовить презентацию и ответить на письма.',
                'tags': ['работа']
            },
            {
                'title': 'Насытить распорядок дня',
                'content': 'Хочу ввести в свой распорядок дня новую привычку - читать 30 минут перед сном.',
                'tags': ['личное', 'идеи']
            },
            {
                'title': 'Города, которые я хочу посетить',
                'content': 'Хочу посетить Калининград, Казань, Самару. Нужно составить план путешествия.',
                'tags': ['путешествия', 'идеи']
            }
        ]

        created_count = 0
        for entry_data in demo_entries:
            # Проверяем, существует ли уже запись с таким заголовком
            if not Entry.objects.filter(title=entry_data['title'], author=user).exists():
                entry = Entry.objects.create(
                    title=entry_data['title'],
                    content=entry_data['content'],
                    author=user
                )

                # Добавляем соответствующие теги
                entry_tags = []
                for tag_name in entry_data['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    entry_tags.append(tag)

                entry.tags.set(entry_tags)
                created_count += 1
                self.stdout.write(f'✅ Создана запись: {entry_data["title"]}')
            else:
                self.stdout.write(f'ℹ️ Запись уже существует: {entry_data["title"]}')

        self.stdout.write(
            self.style.SUCCESS(f'🎉 Успешно создано {created_count} демо-записей!')
        )
        self.stdout.write(
            self.style.SUCCESS('👤 Для входа используйте: email: demo@example.com, password: demo123')
        )
