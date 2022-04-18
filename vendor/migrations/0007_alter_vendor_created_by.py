# Generated by Django 4.0.4 on 2022-04-16 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendor', '0006_alter_vendor_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='created_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL),
        ),
    ]
