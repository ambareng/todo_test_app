from django.contrib import admin

from todo_app.models import Todo, TodoList

admin.site.register(Todo)
admin.site.register(TodoList)
