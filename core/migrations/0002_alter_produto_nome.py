# Generated by Django 5.1.4 on 2024-12-14 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome'),
        ),
    ]
