# Generated by Django 3.2.23 on 2023-12-27 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='posts',
        ),
    ]
