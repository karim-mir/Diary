from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load initial data with migrations'

    def handle(self, *args, **options):
        # Применить миграции
        self.stdout.write('Applying migrations...')
        call_command('migrate')

        # Загрузить фикстуры
        self.stdout.write('Loading initial data...')
        call_command('loaddata', 'fixtures/initial_data.json')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial data!')
        )
