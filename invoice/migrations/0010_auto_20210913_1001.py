# Generated by Django 3.2.5 on 2021-09-13 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_auto_20210901_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseitem',
            options={'ordering': ['purchaseInvoice__date']},
        ),
        migrations.AlterModelOptions(
            name='salesitem',
            options={'ordering': ['salesInvoice__date']},
        ),
    ]