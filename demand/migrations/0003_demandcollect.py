# Generated by Django 3.2 on 2021-05-26 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0002_dimg'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemandCollect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('demandID', models.IntegerField()),
            ],
        ),
    ]
