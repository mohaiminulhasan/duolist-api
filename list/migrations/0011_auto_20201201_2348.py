# Generated by Django 3.1.3 on 2020-12-01 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('list', '0010_auto_20201201_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='sender',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
