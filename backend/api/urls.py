from django.urls import path
from . import views

urlpatterns = [
    path('parse-log', views.parse_log, name='parse_log'),
    path('register', views.register, name='register'),
    path('me', views.get_me, name='me'),
]
