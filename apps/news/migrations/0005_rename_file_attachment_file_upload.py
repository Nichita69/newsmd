# Generated by Django 4.1 on 2022-08-29 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_timer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='file',
            new_name='file_upload',
        ),
    ]
