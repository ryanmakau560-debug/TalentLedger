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
path('api/users/', views.list_users, name='user-list'),
path('requests/', views.received_requests_view, name='received_requests'),
path('toggle-booking/<int:skill_id>/', views.toggle_book_session, name='toggle_booking'),
    
]