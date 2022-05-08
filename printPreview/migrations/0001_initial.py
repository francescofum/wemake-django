# Generated by Django 4.0.4 on 2022-05-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='STL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('file', models.FileField(upload_to='STL')),
                ('pretty_name', models.CharField(max_length=255)),
                ('upload_data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
