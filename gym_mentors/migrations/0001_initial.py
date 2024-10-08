# Generated by Django 5.1 on 2024-09-06 17:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gym_details', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentors',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('expertise', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=20)),
                ('Gym', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mentors', to='gym_details.gymdetails')),
            ],
        ),
    ]
