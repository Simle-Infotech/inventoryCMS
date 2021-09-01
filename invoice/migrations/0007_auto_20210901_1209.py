# Generated by Django 3.2.5 on 2021-09-01 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0011_shoppingitems_price'),
        ('invoice', '0006_auto_20210901_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='salesitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='qty',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='salesinvoice',
            name='order_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.shoppingcart'),
        ),
        migrations.AddField(
            model_name='salesitem',
            name='qty',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='expiryDate',
            field=models.DateField(blank=True, null=True, verbose_name='Expiry Date'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesitem',
            name='expiryDate',
            field=models.DateField(blank=True, null=True, verbose_name='Expiry Date'),
        ),
        migrations.AlterField(
            model_name='salesitem',
            name='rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]