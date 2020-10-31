# Generated by Django 3.1.2 on 2020-10-26 14:00

import Store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', 'alkdj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(default='Aurangabad'),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.IntegerField(default=9876543210, validators=[Store.models.validate_contact_number]),
        ),
    ]