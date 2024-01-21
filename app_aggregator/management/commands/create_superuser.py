from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from app_aggregator.models import User


class Command(BaseCommand):
    help = "Creates Bulk Users with Aggregator User Type"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username')
        parser.add_argument('--password', type=str, help='Password')
        parser.add_argument('--email', type=str, help='Email ID')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        try:
            User.objects.create(username=username, password=make_password(password), email=email, is_superuser=True)
            self.stdout.write(self.style.SUCCESS('Admin Created'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
