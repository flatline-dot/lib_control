# Generated by Django 3.2.13 on 2022-06-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0012_auto_20220601_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_book',
            field=models.CharField(max_length=80, unique=True, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=80, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre_book',
            field=models.CharField(max_length=80, unique=True, verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=80, unique=True),
        ),
    ]