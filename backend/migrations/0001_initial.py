# Generated by Django 2.2.3 on 2020-07-25 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.TextField(max_length=255)),
                ('last_name', models.TextField(max_length=255)),
                ('address', models.TextField()),
                ('dob', models.DateField()),
                ('company', models.TextField(max_length=100)),
                ('card_id', models.TextField(blank=True)),
            ],
        ),
    ]