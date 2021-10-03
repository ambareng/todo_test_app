from rest_framework import serializers

from todo_app.models import Todo, TodoList


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name']


class TodoAdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'todo_list']


class TodoListSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(source='todo_set', many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = ['id', 'user', 'name', 'todos', 'created_at', 'updated_at']
