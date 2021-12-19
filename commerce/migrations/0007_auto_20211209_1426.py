# Generated by Django 3.2.8 on 2021-12-09 22:26

import commerce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0006_useruploadedimage_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='images',
        ),
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to=commerce.models.upload_to),
        ),
    ]