# Generated by Django 3.2.5 on 2021-09-01 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0002_invoice_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='invoice',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='Items',
        ),
    ]