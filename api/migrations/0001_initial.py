# Generated by Django 5.2.1 on 2025-05-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start", models.DateTimeField(auto_now_add=True)),
                ("end", models.DateTimeField(blank=True, null=True)),
                ("state", models.CharField(default="         ", max_length=9)),
            ],
        ),
    ]
