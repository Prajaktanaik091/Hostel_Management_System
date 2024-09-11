# Generated by Django 5.0.7 on 2024-08-31 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_roomate"),
    ]

    operations = [
        migrations.CreateModel(
            name="Complaints",
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
                ("room_number", models.CharField(max_length=4)),
                ("complain", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
