from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from todo_app.models import Todo, TodoList
from todo_app.serializers import TodoListSerializer, TodoSerializer, TodoAdditionalSerializer


class TodoListsAPIView(APIView):
    @staticmethod
    def get(request):
        todo_lists = TodoList.objects.all()
        serializer = TodoListSerializer(todo_lists, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = TodoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class TodoListDetailsAPIView(APIView):
    @staticmethod
    def get(request, pk):
        todo_list = get_object_or_404(TodoList, id=pk)
        serializer = TodoListSerializer(todo_list)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        todo_list = get_object_or_404(TodoList, id=pk)
        serializer = TodoListSerializer(todo_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @staticmethod
    def delete(request, pk):
        todo_list = get_object_or_404(TodoList, id=pk)
        todo_list.delete()
        return Response(status=204)


class TodoAPIView(ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoAdditionalSerializer


class TodoDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoAdditionalSerializer
