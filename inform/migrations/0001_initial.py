# Generated by Django 3.2 on 2021-06-04 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inform',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('userid', models.IntegerField()),
                ('text', models.CharField(max_length=100)),
                ('isread', models.BooleanField()),
                ('score', models.BooleanField()),
            ],
        ),
    ]
