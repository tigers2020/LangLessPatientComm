# Generated by Django 5.0.6 on 2024-06-27 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0007_drug_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drug',
            name='generic_name',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='manufacturer_name',
        ),
    ]
