# Generated by Django 4.2.5 on 2024-02-05 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_usymptoms_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usymptoms',
            name='userchat',
            field=models.TextField(blank=True, null=True),
        ),
    ]
