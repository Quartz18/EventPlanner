# Generated by Django 3.0.5 on 2021-03-25 08:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorMore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone No. must be entered in the format +919999999999.', regex='^\\+?1?\\d{9,10}$')], verbose_name='Phone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]