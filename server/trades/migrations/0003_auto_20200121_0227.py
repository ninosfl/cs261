# Generated by Django 3.0.2 on 2020-01-21 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_auto_20200121_0222'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurrencyValues',
            new_name='CurrencyValue',
        ),
        migrations.RenameModel(
            old_name='DerivativeTrades',
            new_name='DerivativeTrade',
        ),
        migrations.RenameModel(
            old_name='ProductPrices',
            new_name='ProductPrice',
        ),
        migrations.RenameModel(
            old_name='StockPrices',
            new_name='StockPrice',
        ),
    ]
