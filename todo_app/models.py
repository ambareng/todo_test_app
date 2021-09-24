import uuid

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Todo(BaseModel):
    name = models.CharField(max_length=255)
    todo_list = models.ForeignKey('TodoList', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TodoList(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
