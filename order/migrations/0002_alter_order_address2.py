# Generated by Django 4.0.4 on 2022-05-10 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
