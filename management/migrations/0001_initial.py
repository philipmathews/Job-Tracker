# Generated by Django 2.0.5 on 2018-05-18 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applied',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('job_title', models.CharField(max_length=200)),
                ('applied', models.DateField(verbose_name='date applied')),
                ('deadline', models.DateField(null=True)),
                ('location', models.CharField(max_length=200, null=True)),
                ('salary', models.IntegerField(null=True)),
                ('post_url', models.URLField(max_length=2000, null=True)),
                ('status', models.TextField(null=True)),
                ('offer', models.DateField(null=True, verbose_name='offer date')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('job_title', models.CharField(max_length=200)),
                ('deadline', models.DateField(null=True)),
                ('applied', models.DateField(null=True, verbose_name='date applied')),
                ('location', models.CharField(max_length=200, null=True)),
                ('salary', models.IntegerField(null=True)),
                ('post_url', models.URLField(max_length=2000, null=True)),
                ('status', models.TextField(null=True)),
                ('offer', models.DateField(null=True, verbose_name='offer date')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
