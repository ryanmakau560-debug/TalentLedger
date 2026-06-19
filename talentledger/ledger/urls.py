from django.urls import path
from . import views


urlpatterns = [
    path('api/test/', views.test_postman, name='test_postman'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/<str:tier>/', views.payment_view, name='payment'),
    path('api/skills/', views.skill_api_list, name='skill-api'),
    path('api/skills/<int:pk>/', views.skill_detail, name='skill-detail'),
]