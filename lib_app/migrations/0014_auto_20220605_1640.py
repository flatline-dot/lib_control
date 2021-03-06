# Generated by Django 3.2.13 on 2022-06-05 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0013_auto_20220601_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_author',
            field=models.ForeignKey(max_length=80, on_delete=django.db.models.deletion.CASCADE, to='lib_app.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_genre',
            field=models.ForeignKey(max_length=80, on_delete=django.db.models.deletion.CASCADE, to='lib_app.genre', verbose_name='Жанр'),
        ),
    ]
