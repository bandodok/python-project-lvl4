# Generated by Django 3.2.9 on 2021-11-06 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]