# Generated by Django 4.1.13 on 2023-12-13 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_core', '0002_alter_users_password'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='users',
            table='users',
        ),
    ]
