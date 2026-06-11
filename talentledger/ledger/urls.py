from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.test_postman, name='test_postman'),
]