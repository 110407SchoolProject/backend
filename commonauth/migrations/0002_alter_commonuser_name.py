# Generated by Django 3.2 on 2021-08-24 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonuser',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='姓名'),
        ),
    ]
