# Generated by Django 3.1.4 on 2020-12-29 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_patient_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='company',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]