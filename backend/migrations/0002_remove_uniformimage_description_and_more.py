# Generated by Django 4.1.5 on 2023-11-26 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uniformimage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='uniformimage',
            name='is_main',
        ),
    ]