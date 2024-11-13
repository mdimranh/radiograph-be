# Generated by Django 5.1.2 on 2024-11-13 04:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_fee'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radiographerprofile',
            name='department',
        ),
        migrations.AddField(
            model_name='radiographerprofile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radiographer_department', to='account.department'),
        ),
    ]
