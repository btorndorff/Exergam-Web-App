# Generated by Django 3.1.7 on 2021-04-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exergam', '0008_auto_20210417_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usernm',
            field=models.CharField(default='Exergam User', max_length=40),
        ),
    ]
