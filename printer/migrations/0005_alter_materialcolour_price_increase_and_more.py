# Generated by Django 4.0.4 on 2022-04-12 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0004_alter_materialcolour_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialcolour',
            name='price_increase',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='materialcolour',
            name='price_length',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=6),
        ),
    ]
