from django.urls import path
from . import views
from .views import set_user_password, simple_login, simple_signup

urlpatterns = [
    path("api/auth/set-password/", set_user_password),
    path("api/auth/login/", simple_login),
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
path('book-session/<int:skill_id>/', views.toggle_book_session, name='book_session'),
path('api/skills/<int:skill_id>/book/', views.api_book_skill, name='api-book-skill'),
    path('api/instructor/requests/', views.api_instructor_requests, name='api-instructor-requests'),
    path('api/transactions/<int:transaction_id>/respond/', views.api_respond_booking, name='api-respond-booking'),
    path('api/my-bookings/', views.api_my_bookings, name='api-my-bookings'),
    path('api/transactions/<int:pk>/award-credit/', views.award_booking_credit, name='award-booking-credit'),
    path("api/auth/signup/", simple_signup),
    
]