# Generated by Django 3.2 on 2021-05-24 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DImg',
            fields=[
                ('imgid', models.IntegerField(primary_key=True, serialize=False)),
                ('demandid', models.IntegerField(blank=True)),
                ('img', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]
