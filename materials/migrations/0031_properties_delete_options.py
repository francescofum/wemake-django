# Generated by Django 4.0.4 on 2022-04-22 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('materials', '0030_alter_options_owned_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.BooleanField(default=True)),
                ('price_length', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('discount', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('colour', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='colour_global', to='core.colour_global')),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='colours', to='materials.material')),
            ],
            options={
                'unique_together': {('colour', 'owned_by')},
            },
        ),
        migrations.DeleteModel(
            name='Options',
        ),
    ]
