# Generated by Django 5.0.6 on 2024-06-25 17:29

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_teammember_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
