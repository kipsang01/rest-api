# Generated by Django 4.1 on 2023-09-11 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='message_sent',
            field=models.BooleanField(default=False),
        ),
    ]
