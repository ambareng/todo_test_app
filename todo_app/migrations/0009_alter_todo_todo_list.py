# Generated by Django 3.2.7 on 2021-10-03 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0008_todolist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='todo_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_list', to='todo_app.todolist'),
        ),
    ]
