# Generated by Django 4.0.2 on 2022-03-25 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockCompta', '0009_alter_article_addeddate_alter_bill_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='priceClass',
            new_name='price_Class',
        ),
    ]
