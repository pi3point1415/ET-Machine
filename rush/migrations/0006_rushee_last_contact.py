# Generated by Django 5.0.7 on 2024-07-20 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0005_alter_rushee_options_alter_rushee_dorm'),
    ]

    operations = [
        migrations.AddField(
            model_name='rushee',
            name='last_contact',
            field=models.DateField(blank=True, null=True),
        ),
    ]