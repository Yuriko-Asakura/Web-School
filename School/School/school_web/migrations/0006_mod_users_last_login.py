# Generated by Django 5.1.6 on 2025-02-17 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_web', '0005_alter_mod_users_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod_users',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
