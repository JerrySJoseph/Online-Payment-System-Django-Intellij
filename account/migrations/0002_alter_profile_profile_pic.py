# Generated by Django 4.1.7 on 2023-03-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='panda.png', upload_to='profile_images'),
        ),
    ]
