# Generated by Django 4.1 on 2022-08-29 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_rename_file_attachment_file_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='file_size',
            field=models.IntegerField(default=0),
        ),
    ]
