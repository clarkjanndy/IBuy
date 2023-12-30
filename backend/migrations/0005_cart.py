# Generated by Django 4.2.8 on 2023-12-30 02:31

import backend.models.cart
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('variant', models.CharField(max_length=100)),
                ('expiry_date', models.DateTimeField(default=backend.models.cart.default_expiration_date)),
                ('uniform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_cart_items', to='backend.uniform')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
