# Generated by Django 5.1 on 2024-09-06 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        ('gym_details', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymattendance',
            name='gym',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym_details.gymdetails'),
        ),
    ]
