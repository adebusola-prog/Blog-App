# Generated by Django 4.1.2 on 2022-10-19 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ourblog", "0020_alter_post_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-created_at"],
                "permissions": (("can_delete_post", "Set to delete post"),),
            },
        ),
    ]
