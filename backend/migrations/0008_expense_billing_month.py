# Generated by Django 4.2.8 on 2024-03-21 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='billing_month',
            field=models.DateField(default=datetime.datetime(2024, 3, 21, 13, 29, 37, 692413, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
