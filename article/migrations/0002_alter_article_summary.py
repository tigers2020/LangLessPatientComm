# Generated by Django 5.0.6 on 2024-07-03 18:24

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=ckeditor.fields.RichTextField(blank=True, max_length=500),
        ),
    ]
