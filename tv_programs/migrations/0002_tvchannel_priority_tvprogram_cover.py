# Generated by Django 5.1.4 on 2025-01-09 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv_programs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvchannel',
            name='priority',
            field=models.IntegerField(default=0, verbose_name='Приоритет'),
        ),
        migrations.AddField(
            model_name='tvprogram',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='tv/covers', verbose_name='Обложка'),
        ),
    ]
