# Generated by Django 2.2.3 on 2019-08-26 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_auto_20190820_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='traktor_id',
        ),
        migrations.DeleteModel(
            name='TraktorInfo',
        ),
    ]
