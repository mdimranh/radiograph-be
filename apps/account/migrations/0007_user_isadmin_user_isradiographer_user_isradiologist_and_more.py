# Generated by Django 5.1.2 on 2024-11-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_radiologist_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='isRadiographer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='isRadiologist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='radiologist',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatars', verbose_name='Avatar'),
        ),
    ]
