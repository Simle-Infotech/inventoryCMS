# Generated by Django 3.2.5 on 2021-08-20 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_dealermeta_dealer'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertype',
            name='belongs_to_customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.customer'),
        ),
    ]
