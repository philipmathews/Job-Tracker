# Generated by Django 2.0.5 on 2018-05-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(null=True, verbose_name='created date'),
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]