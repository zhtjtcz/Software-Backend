# Generated by Django 3.2 on 2021-05-25 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userfollow'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCollect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('goodID', models.IntegerField()),
            ],
        ),
    ]
