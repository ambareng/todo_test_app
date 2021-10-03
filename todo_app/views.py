import jwt

from auth.authentications import JWTAuthentication

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import get_authorization_header

from todo_app.models import Todo, TodoList
from todo_app.serializers import TodoListSerializer, TodoAdditionalSerializer


class TodoListsAPIView(APIView):
    @staticmethod
    def get(request):
        current_user = JWTAuthentication.get_current_user(request)
        if current_user.is_superuser:
            todo_lists = TodoList.objects.all()
        else:
            todo_lists = TodoList.objects.filter(user=current_user)
        serializer = TodoListSerializer(todo_lists, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = TodoListSerializer(data=request.data)
        if serializer.is_valid():
            current_user = JWTAuthentication.get_current_user(request)
            serializer.save(user=current_user)
            return Response(serializer.data)
        return Response(serializer.errors)


class TodoListDetailsAPIView(APIView):
    @staticmethod
    def get(request, pk):
        current_user = JWTAuthentication.get_current_user(request)
        if current_user.is_superuser:
            todo_list = get_object_or_404(TodoList, id=pk)
        else:
            todo_list = get_object_or_404(TodoList, id=pk, user=current_user)
        serializer = TodoListSerializer(todo_list)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        current_user = JWTAuthentication.get_current_user(request)
        if current_user.is_superuser:
            todo_list = get_object_or_404(TodoList, id=pk)
        else:
            todo_list = get_object_or_404(TodoList, id=pk, user=current_user)
        serializer = TodoListSerializer(todo_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @staticmethod
    def delete(request, pk):
        current_user = JWTAuthentication.get_current_user(request)
        if current_user.is_superuser:
            todo_list = get_object_or_404(TodoList, id=pk)
        else:
            todo_list = get_object_or_404(TodoList, id=pk, user=current_user)
        todo_list.delete()
        return Response(status=204)


class TodoAPIView(ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoAdditionalSerializer

    # def get(self, request, *args, **kwargs):
    #     current_user = JWTAuthentication.get_current_user(request)
    #     if current_user.is_superuser:
    #         todos = Todo.objects.all()
    #     else:
    #         todos = Todo.objects.filter(user=current_user)
    #     serializer = TodoAdditionalSerializer(todos, many=True)
    #     return Response(serializer.data)


class TodoDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoAdditionalSerializer
