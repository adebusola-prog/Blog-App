# Generated by Django 4.1.2 on 2022-10-24 17:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ourblog", "0028_alter_post_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="blog_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
