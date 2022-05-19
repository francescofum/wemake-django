# Generated by Django 4.0.4 on 2022-05-19 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('PEND', 'Pending'), ('RECV', 'Received'), ('PRINT', 'Printing'), ('FINISHING', 'Finishing'), ('CMPLT', 'Complete'), ('DELIV', 'Sent')], default='PEND', max_length=50)),
                ('vendor_paid', models.CharField(choices=[('PEND', 'Pending'), ('RECV', 'Received'), ('PRINT', 'Printing'), ('FINISHING', 'Finishing'), ('CMPLT', 'Complete'), ('DELIV', 'Sent')], default='NO', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('price_total', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_shipping', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('shipping_type', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='vendor.vendor')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pretty_name', models.TextField(blank=True, null=True)),
                ('material', models.CharField(max_length=255)),
                ('colour', models.CharField(max_length=255)),
                ('infill', models.DecimalField(decimal_places=0, default=0, max_digits=6)),
                ('url', models.CharField(max_length=255)),
                ('dim_x', models.DecimalField(decimal_places=0, max_digits=6)),
                ('dim_y', models.DecimalField(decimal_places=0, max_digits=6)),
                ('dim_z', models.DecimalField(decimal_places=0, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
            ],
        ),
    ]
