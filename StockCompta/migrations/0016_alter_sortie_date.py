# Generated by Django 4.0.2 on 2022-04-14 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockCompta', '0015_alter_bill_numero_evolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sortie',
            name='Date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
