# Generated by Django 5.1.4 on 2025-02-08 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_event_ticket_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='curr_ticket',
            field=models.IntegerField(default=0),
        ),
    ]
