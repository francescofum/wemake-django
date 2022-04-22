# Generated by Django 4.0.4 on 2022-04-22 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_material_global_global_material'),
        ('materials', '0034_rename_name_material_global_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.BooleanField(default=True)),
                ('price_coefficient', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('discount', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('global_colours', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='colour_global', to='core.colour_global')),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='colours', to='materials.material')),
            ],
            options={
                'verbose_name': 'Colour',
                'verbose_name_plural': 'Material Properties',
                'unique_together': {('global_colours', 'owned_by')},
            },
        ),
        migrations.DeleteModel(
            name='Property',
        ),
    ]
