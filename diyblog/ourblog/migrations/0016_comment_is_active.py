# Generated by Django 4.1.2 on 2022-10-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ourblog", "0015_alter_comment_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]