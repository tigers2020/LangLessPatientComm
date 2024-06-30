# Generated by Django 5.0.6 on 2024-06-27 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0005_rename_symptoms_drug_uses_remove_drug_dosage_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='full_product_details',
            field=models.FileField(blank=True, null=True, upload_to='product_details/'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='generic_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='drug',
            name='manufacturer_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]