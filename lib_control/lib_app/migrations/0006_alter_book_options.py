# Generated by Django 4.0.1 on 2022-03-07 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0005_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-book_author']},
        ),
    ]