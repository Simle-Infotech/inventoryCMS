# Generated by Django 3.2.5 on 2021-08-24 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_color_hash_code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemcoloravailability',
            unique_together={('item', 'color')},
        ),
    ]