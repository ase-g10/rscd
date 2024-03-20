# Generated by Django 4.2.7 on 2024-03-19 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_log_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='disaster',
            name='is_verified',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='disaster',
            name='radius',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='disaster',
            name='type',
            field=models.CharField(choices=[('Car Accident', 'Car Accident'), ('Fire Disaster', 'Fire Disaster'), ('Riot', 'Riot')], default='Car Accident', max_length=40),
        ),
        migrations.AlterField(
            model_name='log',
            name='create_time',
            field=models.CharField(max_length=255),
        ),
    ]