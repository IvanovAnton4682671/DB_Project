# Generated by Django 4.1.13 on 2023-12-19 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_core', '0003_alter_users_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=40)),
                ('album', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'music_base',
            },
        ),
    ]