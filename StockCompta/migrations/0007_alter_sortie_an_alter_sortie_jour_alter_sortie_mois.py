# Generated by Django 4.0.2 on 2022-03-13 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockCompta', '0006_remove_sortie_takedate_sortie_an_sortie_jour_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sortie',
            name='an',
            field=models.CharField(default=2022, max_length=15),
        ),
        migrations.AlterField(
            model_name='sortie',
            name='jour',
            field=models.CharField(default=13, max_length=15),
        ),
        migrations.AlterField(
            model_name='sortie',
            name='mois',
            field=models.CharField(default=3, max_length=15),
        ),
    ]
