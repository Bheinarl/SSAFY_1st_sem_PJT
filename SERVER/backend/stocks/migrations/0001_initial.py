# Generated by Django 4.2.4 on 2024-12-16 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsHeadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('headline', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
            ],
        ),
    ]