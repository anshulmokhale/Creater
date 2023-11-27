from django.urls import path
from .views import display_demo, user_input

urlpatterns = [
    path('display_demo/', display_demo, name='display_demo'),
    path('user_input/', user_input, name='user_input'),
]
