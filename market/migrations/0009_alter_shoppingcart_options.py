# Generated by Django 3.2.5 on 2021-08-26 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_alter_shoppingcart_paid_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ('-cart_created', '-paid_status')},
        ),
    ]