# Generated by Django 4.1.1 on 2022-12-23 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "experiences",
            "0003_alter_experience_category_alter_experience_host_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="max_guests",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
