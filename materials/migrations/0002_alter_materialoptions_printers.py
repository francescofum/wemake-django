# Generated by Django 4.0.4 on 2022-04-16 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0016_remove_materialoptions_colour_and_more'),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialoptions',
            name='printers',
            field=models.ManyToManyField(related_name='materials', to='printer.printer'),
        ),
    ]
