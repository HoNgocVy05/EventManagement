# Generated by Django 5.1.4 on 2025-02-03 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_event_initial_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='initial_tickets',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
