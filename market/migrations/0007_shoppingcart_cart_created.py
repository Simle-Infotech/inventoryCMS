# Generated by Django 3.2.5 on 2021-08-25 02:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_auto_20210825_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='cart_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]