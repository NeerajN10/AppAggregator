from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError

from app_aggregator.model_choices import UserTypes
from app_aggregator.models import User
import pandas as pd


class Command(BaseCommand):
    help = "Creates Bulk Users with Aggregator User Type"

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        excel_file_path = options['excel_file']

        try:
            # Read Excel file into a DataFrame
            df = pd.read_excel(excel_file_path)

            # Loop through DataFrame and create User obj list
            user_list = []
            for _, row in df.iterrows():
                user_list.append(
                    User(
                        username=row['username'],
                        type=UserTypes.AGGREGATOR if row['type'] == UserTypes.AGGREGATOR.name else UserTypes.USER,
                        password=make_password(row['password'])
                    )
                )

            if user_list:
                User.objects.bulk_create(user_list)

            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
