# Generated by Django 2.2.3 on 2020-07-26 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200726_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='sub_date',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='sub_id',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='sub_name',
        ),
    ]
