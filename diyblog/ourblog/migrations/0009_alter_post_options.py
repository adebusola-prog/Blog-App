# Generated by Django 4.1.2 on 2022-10-14 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ourblog", "0008_alter_post_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-created_at"],
                "permissions": (("can_update_post", "Set to update post"),),
            },
        ),
    ]