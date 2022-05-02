# Generated by Django 4.0.4 on 2022-05-02 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('store_name', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('store_logo_raw', models.ImageField(blank=True, null=True, upload_to='')),
                ('store_logo_thumbnail', models.ImageField(blank=True, null=True, upload_to='')),
                ('created_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_by'],
            },
        ),
    ]
