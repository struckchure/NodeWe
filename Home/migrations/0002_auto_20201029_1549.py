# Generated by Django 3.1.2 on 2020-10-29 14:49

import Home.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, default='default_avatar', upload_to=Home.utils.course_cover_upload_handler),
        ),
    ]
