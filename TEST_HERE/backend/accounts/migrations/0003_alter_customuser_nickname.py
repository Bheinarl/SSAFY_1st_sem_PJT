# Generated by Django 4.2.4 on 2024-11-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_age_alter_customuser_interests_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
