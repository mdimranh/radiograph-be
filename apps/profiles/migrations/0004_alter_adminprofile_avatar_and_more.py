# Generated by Django 5.1.2 on 2024-11-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_certificate_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='radiographerprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='radiologistprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
    ]
