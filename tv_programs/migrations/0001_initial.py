# Generated by Django 5.1.4 on 2025-01-03 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TVChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='tv/channels', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Телеканал',
                'verbose_name_plural': 'Телеканалы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TVProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('tv_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv_programs.tvchannel', verbose_name='ID Телеканала')),
            ],
            options={
                'verbose_name': 'Телепрограммы',
                'ordering': ['date'],
            },
        ),
    ]
