# Generated by Django 4.1.2 on 2022-10-19 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ourblog", "0025_category_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]