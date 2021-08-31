# Generated by Django 3.2 on 2021-08-25 10:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('commonauth', '0003_auto_20210825_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonuser',
            name='userid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='使用者ID'),
        ),
    ]
