# Generated by Django 5.0.6 on 2024-07-11 17:15

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0014_alter_route_options_alter_route_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='route',
            options={},
        ),
        migrations.AlterField(
            model_name='drug',
            name='dosage',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
        migrations.AlterField(
            model_name='drug',
            name='ingredients',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
        migrations.AlterField(
            model_name='route',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
    ]
