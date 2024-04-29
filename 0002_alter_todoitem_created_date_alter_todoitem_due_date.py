# Generated by Django 4.2.11 on 2024-04-27 19:33

from django.db import migrations, models
import todo_app.models


class Migration(migrations.Migration):
    dependencies = [
        ("todo_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todoitem",
            name="created_date",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="todoitem",
            name="due_date",
            field=models.DateTimeField(
                db_index=True, default=todo_app.models.ten_day_hence
            ),
        ),
    ]
