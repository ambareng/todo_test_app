from django.urls import path

from auth.views import Register

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
]
