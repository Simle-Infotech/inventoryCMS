# Generated by Django 3.2.5 on 2021-09-13 04:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_itemcoloravailability_unique_together'),
        ('inventory', '0006_auto_20210913_0823'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinginventory',
            options={'ordering': ['-entry_date']},
        ),
        migrations.AddField(
            model_name='inventorycount',
            name='count_updated_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='inventorycount',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.itemcoloravailability'),
        ),
        migrations.AlterField(
            model_name='openinginventory',
            name='expiry',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Expiry Date'),
        ),
    ]
