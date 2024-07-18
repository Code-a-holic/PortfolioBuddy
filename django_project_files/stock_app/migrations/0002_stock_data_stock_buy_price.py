# Generated by Django 4.2.13 on 2024-06-30 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.TextField()),
                ('date', models.TextField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('avg_price', models.FloatField()),
                ('turn_over_in_cr', models.FloatField()),
                ('delivery_percentage', models.FloatField()),
                ('delivery_in_cr', models.FloatField()),
                ('buy_price', models.FloatField()),
                ('percentage_difference', models.FloatField()),
                ('username', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='buy_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
