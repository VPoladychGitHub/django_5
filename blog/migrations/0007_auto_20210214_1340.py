# Generated by Django 3.1.5 on 2021-02-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210214_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'unpublished'), (2, 'published')], default=1),
        ),
    ]