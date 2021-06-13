# Generated by Django 3.2 on 2021-06-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inform', '0003_rename_infromid_score_informid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Informs',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('userid', models.IntegerField()),
                ('text', models.CharField(max_length=100)),
                ('isread', models.BooleanField()),
                ('score', models.BooleanField()),
                ('date', models.CharField(max_length=100)),
                ('goodid', models.IntegerField()),
                ('demandid', models.IntegerField()),
            ],
        ),
    ]