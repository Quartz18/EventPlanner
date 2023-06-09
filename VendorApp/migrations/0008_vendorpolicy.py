# Generated by Django 3.0.5 on 2021-03-29 20:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VendorApp', '0007_venuepolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='CATERER', max_length=20)),
                ('vendor_yrs_exp', models.IntegerField(default=0)),
                ('events_completed', models.IntegerField(default=0)),
                ('vendor_usp', models.TextField(default='None')),
                ('travel_allowance', models.BooleanField(default=False)),
                ('outside_travel_price', models.BooleanField(default=False)),
                ('advance_percentage', models.IntegerField(default=25, validators=[django.core.validators.MaxValueValidator(100, message='Value cannot be more than 100%')])),
                ('cancellation', models.BooleanField(default=False)),
                ('vendor_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='VendorApp.UpperVendor')),
            ],
        ),
    ]
