# Generated by Django 5.0.6 on 2024-06-25 17:08

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('image_src', models.ImageField(blank=True, null=True, upload_to='team_images/')),
            ],
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
    ]
