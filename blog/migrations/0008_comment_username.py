# Generated by Django 3.1.5 on 2021-02-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210214_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(default='', max_length=100, verbose_name='username'),
        ),
    ]
