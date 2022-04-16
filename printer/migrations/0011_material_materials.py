# Generated by Django 4.0.4 on 2022-04-12 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0010_remove_printer_materials'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='materials',
            field=models.ManyToManyField(related_name='material', to='printer.printer'),
        ),
    ]
