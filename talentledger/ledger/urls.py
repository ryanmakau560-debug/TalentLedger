from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.test_postman, name='test_postman'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('marketplace/', views.marketplace, name='marketplace'),
]