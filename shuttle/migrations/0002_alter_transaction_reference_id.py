# Generated by Django 5.0.3 on 2024-04-12 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuttle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reference_id',
            field=models.CharField(default='0d8625e4bb9544c69aa1c18f8060cb94', max_length=255, unique=True),
        ),
    ]
