# Generated by Django 3.1.3 on 2020-11-20 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0003_auto_20201119_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]