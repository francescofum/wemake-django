# Generated by Django 4.0.4 on 2022-04-18 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0015_alter_vendor_store_logo_raw_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='store_logo_raw',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='store_logo_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
