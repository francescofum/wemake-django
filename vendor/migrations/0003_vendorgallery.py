# Generated by Django 4.0.4 on 2022-06-07 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_vendor_gallery_img_1_vendor_gallery_img_2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='vendor.vendor')),
            ],
        ),
    ]
