# Generated by Django 3.2.5 on 2021-08-20 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210820_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcoloravailability',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.color'),
        ),
    ]