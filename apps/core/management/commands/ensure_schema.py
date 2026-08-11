import os
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Crée le schéma Postgres avant les migrations."

    def handle(self, *args, **options):
        schema = os.environ.get('DB_SCHEMA', 'infinityhome')
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
        self.stdout.write(self.style.SUCCESS(f'Schéma "{schema}" créé/vérifié.'))