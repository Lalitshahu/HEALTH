# Generated by Django 4.2.5 on 2024-01-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_remove_mprofile_userfile_mprofile_userage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mprofile',
            name='userimg',
            field=models.ImageField(null=True, upload_to='static/image'),
        ),
    ]
