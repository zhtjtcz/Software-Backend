# Generated by Django 3.2 on 2021-06-03 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('objectID', models.IntegerField()),
                ('type', models.IntegerField()),
                ('ownID', models.IntegerField()),
                ('requestID', models.IntegerField()),
                ('status', models.IntegerField()),
                ('score', models.FloatField()),
            ],
        ),
    ]
