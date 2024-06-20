
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Load SQL script into the database'

    def handle(self, *args, **options):
        # Path to your SQL script
        sql_script_path = 'script.sql'

        with connection.cursor() as cursor:
            with open(sql_script_path, 'r') as f:
                sql = f.read()
                cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS('SQL script loaded successfully'))
