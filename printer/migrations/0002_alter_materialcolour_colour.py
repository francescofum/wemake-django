# Generated by Django 4.0.4 on 2022-04-12 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialcolour',
            name='colour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='colour', to='printer.colour'),
        ),
    ]
