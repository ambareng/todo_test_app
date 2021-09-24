from django.urls import path

from todo_app.views import TodoListsAPIView, TodoListDetailsAPIView, TodoAPIView, TodoDetailsAPIView

urlpatterns = [
    path('todo_lists/', TodoListsAPIView.as_view(), name='todo_lists'),
    path('todo_list/<uuid:pk>/', TodoListDetailsAPIView.as_view(), name='todo_list_details'),
    path('todos/', TodoAPIView.as_view(), name='todos'),
    path('todo/<uuid:pk>/', TodoDetailsAPIView.as_view(), name='todo_details'),
]
