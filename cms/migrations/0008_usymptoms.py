# Generated by Django 4.2.5 on 2024-02-05 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_alter_mprofile_userage_alter_mprofile_usernumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usymptoms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userheight', models.IntegerField(null=True)),
                ('userweight', models.IntegerField(null=True)),
                ('userchat', models.TextField()),
            ],
        ),
    ]
