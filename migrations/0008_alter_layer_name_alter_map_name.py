# Generated by Django 5.1.6 on 2025-03-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinmap', '0007_rectangle_pinmap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='map',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
