# Generated by Django 3.2 on 2021-08-25 10:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('commonauth', '0004_alter_commonuser_userid'),
        ('diary', '0004_alter_diary_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='diaryid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='日記ID'),
        ),
        migrations.AlterField(
            model_name='diary',
            name='userid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commonauth.commonuser', verbose_name='使用者ID'),
        ),
    ]
