# Generated by Django 4.0.4 on 2022-04-23 17:50

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
                ('zipcode', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price_total', models.DecimalField(decimal_places=2, max_digits=6)),
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
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='vendor.vendor')),
            ],
        ),
    ]
