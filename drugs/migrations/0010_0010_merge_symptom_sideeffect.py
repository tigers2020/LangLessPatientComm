from django.db import migrations, models

def combine_symptoms_and_side_effects(apps, schema_editor):
    Symptom = apps.get_model('drugs', 'Symptom')
    SideEffect = apps.get_model('drugs', 'SideEffect')
    Condition = apps.get_model('drugs', 'Condition')
    Drug = apps.get_model('drugs', 'Drug')

    for symptom in Symptom.objects.all():
        condition = Condition.objects.create(
            name=symptom.name,
            image=symptom.image,
            is_side_effect=False
        )
        for drug in symptom.drugs.all():
            drug.conditions.add(condition)

    for side_effect in SideEffect.objects.all():
        condition = Condition.objects.create(
            name=side_effect.name,
            image=side_effect.image,
            is_side_effect=True
        )
        for drug in side_effect.drugs.all():
            drug.conditions.add(condition)

class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0009_alter_sideeffect_image_alter_symptom_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='conditions/')),
                ('is_side_effect', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='drug',
            name='conditions',
            field=models.ManyToManyField(related_name='drugs', to='drugs.Condition'),
        ),
        migrations.RunPython(combine_symptoms_and_side_effects),
        migrations.RemoveField(
            model_name='drug',
            name='side_effects',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='uses',
        ),
        migrations.DeleteModel(
            name='SideEffect',
        ),
        migrations.DeleteModel(
            name='Symptom',
        ),
    ]