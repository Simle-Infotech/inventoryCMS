# Generated by Django 3.2.5 on 2021-08-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210805_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='album',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ManyToManyField(blank=True, to='products.Image'),
        ),
    ]
