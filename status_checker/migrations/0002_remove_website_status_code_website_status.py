# Generated by Django 4.2.1 on 2024-12-06 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status_checker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='status_code',
        ),
        migrations.AddField(
            model_name='website',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
