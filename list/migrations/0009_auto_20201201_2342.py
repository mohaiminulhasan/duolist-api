# Generated by Django 3.1.3 on 2020-12-01 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0008_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created']},
        ),
    ]
