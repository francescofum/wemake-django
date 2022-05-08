# Generated by Django 4.0.4 on 2022-05-02 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField()),
                ('vendors', models.ManyToManyField(related_name='orders', to='vendor.vendor')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_has_been_paid', models.BooleanField(default=False)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pretty_name', models.TextField(blank=True, null=True)),
                ('material', models.CharField(max_length=255)),
                ('colour', models.CharField(max_length=255)),
                ('dim_x', models.DecimalField(decimal_places=0, max_digits=6)),
                ('dim_y', models.DecimalField(decimal_places=0, max_digits=6)),
                ('dim_z', models.DecimalField(decimal_places=0, max_digits=6)),
                ('infill', models.DecimalField(decimal_places=0, max_digits=6)),
                ('time_to_print', models.DecimalField(decimal_places=0, max_digits=6)),
                ('length_of_filament', models.DecimalField(decimal_places=0, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='vendor.vendor')),
            ],
        ),
    ]
