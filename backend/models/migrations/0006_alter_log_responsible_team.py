# Generated by Django 4.2.7 on 2024-03-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_log_radius_log_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='responsible_team',
            field=models.CharField(max_length=255),
        ),
    ]
