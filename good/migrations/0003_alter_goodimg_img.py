# Generated by Django 3.2 on 2021-05-22 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good', '0002_alter_goodimg_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodimg',
            name='img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
