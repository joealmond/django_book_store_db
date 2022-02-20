# Generated by Django 4.0.2 on 2022-02-20 21:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book_outlet', '0004_author_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='first_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='author',
            name='last_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]