# Generated by Django 5.0.3 on 2024-04-14 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuttle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reference_id',
            field=models.CharField(default='f957644a6d0e4170b4bc58ed2abb3de6', max_length=255, unique=True),
        ),
    ]
