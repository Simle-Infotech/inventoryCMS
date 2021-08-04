# Generated by Django 3.2.5 on 2021-08-01 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_rename_dealermeta_dealer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('title', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('payment_mode', models.IntegerField(choices=[(1, 'Cheque'), (2, 'Cash'), (3, 'Bank Transfer'), (4, 'Internet Payment'), (5, 'Transport'), (6, 'Bank Deposit'), (7, 'Goods Returned'), (8, 'Discount')])),
                ('date', models.DateField(blank=True, null=True)),
                ('nepali_date', models.CharField(blank=True, default='', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cashflow.term')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DealerPaymnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('payment_mode', models.IntegerField(choices=[(1, 'Cheque'), (2, 'Cash'), (3, 'Bank Transfer'), (4, 'Internet Payment'), (5, 'Transport'), (6, 'Bank Deposit'), (7, 'Goods Returned'), (8, 'Discount')])),
                ('date', models.DateField(blank=True, null=True)),
                ('nepali_date', models.CharField(blank=True, default='', max_length=20)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.dealer')),
                ('term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cashflow.term')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpeningBalanceDealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Opening Balance')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.dealer')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashflow.term')),
            ],
            options={
                'abstract': False,
                'unique_together': {('account', 'term')},
            },
        ),
        migrations.CreateModel(
            name='OpeningBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Opening Balance')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashflow.term')),
            ],
            options={
                'abstract': False,
                'unique_together': {('account', 'term')},
            },
        ),
    ]