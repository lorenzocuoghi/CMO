# Generated by Django 2.0.5 on 2018-07-15 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_auto_20180713_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pub_date',
            field=models.DateField(null=True, verbose_name='Data'),
        ),
    ]