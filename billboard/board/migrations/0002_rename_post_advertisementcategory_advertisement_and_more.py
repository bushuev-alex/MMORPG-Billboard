# Generated by Django 4.2.2 on 2023-06-26 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="advertisementcategory",
            old_name="post",
            new_name="advertisement",
        ),
        migrations.RenameField(
            model_name="feedback",
            old_name="post",
            new_name="advertisement",
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("TA", "Танки"),
                    ("HI", "Хилы"),
                    ("DD", "ДД"),
                    ("TR", "Торговцы"),
                    ("GD", "Гилдмастеры"),
                    ("GD", "Квестгиверы"),
                    ("QG", "Уборщик"),
                    ("BS", "Кузнецы"),
                    ("TA", "Кожевники"),
                    ("CO", "Зельевары"),
                    ("MA", "Мастера заклинаний"),
                ],
                default="MA",
                max_length=2,
                unique=True,
            ),
        ),
    ]