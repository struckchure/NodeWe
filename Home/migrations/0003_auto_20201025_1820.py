# Generated by Django 3.1.2 on 2020-10-25 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20201025_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationtoken',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
