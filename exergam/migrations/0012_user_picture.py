# Generated by Django 3.1.7 on 2021-04-18 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exergam', '0011_auto_20210417_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='login.jpeg', upload_to=''),
        ),
    ]
