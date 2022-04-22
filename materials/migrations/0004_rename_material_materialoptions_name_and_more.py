# Generated by Django 4.0.4 on 2022-04-22 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('materials', '0003_alter_materialoptions_printers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialoptions',
            old_name='material',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='materialoptions',
            name='colour',
        ),
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_material', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='material', to='materials.materialoptions')),
                ('colour', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='colour', to='core.colour_global')),
            ],
        ),
    ]
