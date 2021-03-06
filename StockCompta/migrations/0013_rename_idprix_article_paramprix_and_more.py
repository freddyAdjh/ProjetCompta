# Generated by Django 4.0.2 on 2022-03-26 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StockCompta', '0012_alter_article_idprix_alter_bill_idfournisseur_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='idPrix',
            new_name='paramPrix',
        ),
        migrations.RenameField(
            model_name='bill',
            old_name='idFournisseur',
            new_name='paramFournisseur',
        ),
        migrations.RenameField(
            model_name='bill',
            old_name='idUsername',
            new_name='paramUser',
        ),
        migrations.RenameField(
            model_name='sortie',
            old_name='idArticle',
            new_name='paramArticle',
        ),
        migrations.RemoveField(
            model_name='sortie',
            name='idPersonnel',
        ),
        migrations.AddField(
            model_name='sortie',
            name='paramPersonnel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StockCompta.personnel'),
        ),
    ]
