# Generated by Django 3.0.2 on 2020-01-22 17:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0003_derivativetradeproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='derivativetrade',
            name='date_of_trade',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
