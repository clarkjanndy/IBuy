# Generated by Django 4.2.8 on 2024-02-12 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_cart_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='variant',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
