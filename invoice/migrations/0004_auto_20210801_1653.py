# Generated by Django 3.2.5 on 2021-08-01 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20210801_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='expiryDate',
            field=models.DateField(verbose_name='Expiry Date'),
        ),
        migrations.AlterField(
            model_name='salesitem',
            name='expiryDate',
            field=models.DateField(verbose_name='Expiry Date'),
        ),
    ]