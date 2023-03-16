# Generated by Django 3.0.5 on 2021-03-28 11:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Account', '0002_vendormore'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpperVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('VENUE', 'Venue'), ('CATERER', 'Caterer'), ('DECOR', 'Decor'), ('PHOTOGRAPHER', 'Photographer')], default='VENUE', max_length=50, verbose_name='Type')),
                ('vendor_name', models.CharField(max_length=120)),
                ('vendor_about', models.FileField(upload_to='about/%Y/%m/%D')),
                ('vendor_address', models.TextField()),
                ('vendor_contact_name', models.CharField(max_length=100)),
                ('vendor_contact_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message='Phone No. must be entered in the format +919999999999.', regex='^\\+?1?\\d{9,10}$')])),
                ('vendor_taxes', models.CharField(default='F&B : 18.00 %', max_length=20)),
                ('c_log', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.City')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Caterer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('VendorApp.uppervendor',),
        ),
        migrations.CreateModel(
            name='Decor',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('VendorApp.uppervendor',),
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('VendorApp.uppervendor',),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('VendorApp.uppervendor',),
        ),
    ]
