# Generated by Django 3.1.3 on 2020-12-01 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('list', '0009_auto_20201201_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_invites', to=settings.AUTH_USER_MODEL),
        ),
    ]
