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

        user, created = User.objects.get_or_create(username=username, email=email, is_superuser=True)
        if created:
            user.password = make_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Admin Created'))
        elif user:
            self.stdout.write(self.style.SUCCESS('Admin Already exists'))
        else:
            self.stderr.write(self.style.ERROR('Error'))
