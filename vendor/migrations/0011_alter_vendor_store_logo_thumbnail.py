# Generated by Django 4.0.4 on 2022-04-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0010_alter_vendor_store_logo_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='store_logo_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
