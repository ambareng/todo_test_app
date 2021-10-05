import pytest

from django.test import TestCase

from mixer.backend.django import mixer

from todo_app.models import Todo, TodoList


class TestTodoAppModels(TestCase):
    def test_todo_str(self):
        todo = mixer.blend(Todo, name='Clean Stuff')
        assert str(todo) == 'Clean Stuff'

    def test_todo_list_str(self):
        todo_list = mixer.blend(TodoList, name='To do today')
        assert str(todo_list) == 'To do today'
