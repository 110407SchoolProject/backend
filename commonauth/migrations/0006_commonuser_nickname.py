# Generated by Django 3.2 on 2021-09-13 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonauth', '0005_alter_commonuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonuser',
            name='nickname',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='暱稱'),
        ),
    ]