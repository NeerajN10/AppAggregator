# Generated by Django 5.0.1 on 2024-01-21 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_aggregator', '0003_userpurchasedapps_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'AGGREGATOR'), (2, 'USER')], default=1),
        ),
    ]
