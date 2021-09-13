# Generated by Django 3.2 on 2021-08-25 10:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('commonauth', '0002_alter_commonuser_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commonuser',
            old_name='name',
            new_name='truename',
        ),
        migrations.RemoveField(
            model_name='commonuser',
            name='id',
        ),
        migrations.AddField(
            model_name='commonuser',
            name='userid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='commonuser',
            name='birthday',
            field=models.DateField(blank=True, default=None, max_length=128, null=True, verbose_name='生日'),
        ),
        migrations.AlterField(
            model_name='commonuser',
            name='username',
            field=models.EmailField(max_length=128, verbose_name='帳號(信箱)'),
        ),
    ]