# Generated by Django 5.1.2 on 2024-11-07 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_radiologist_delete_rediologist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radiologist',
            name='department',
        ),
        migrations.AddField(
            model_name='radiologist',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radiologists', to='account.department'),
        ),
    ]