# Generated by Django 3.1.7 on 2021-04-17 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exergam', '0006_auto_20210414_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usernm',
            field=models.CharField(default=models.EmailField(max_length=254, unique=True), max_length=40),
        ),
    ]
