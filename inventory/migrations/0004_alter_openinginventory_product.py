# Generated by Django 3.2.5 on 2021-09-05 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_itemcoloravailability_unique_together'),
        ('inventory', '0003_rename_opening_inventory_openinginventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinginventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.itemcoloravailability'),
        ),
    ]