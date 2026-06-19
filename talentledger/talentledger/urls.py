"""
URL configuration for talentledger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ledger.views import delete_skill_view, payment_view, profile_view, skill_api_list,skills_view
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from ledger.views import dashboard_view, add_skill_view, delete_skill_view, register_view
from ledger.views import display_view
from ledger.views import about_view
from ledger.views import subscription_view


urlpatterns = [
    path('', display_view, name='display'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard/')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/profile/', profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-skill/', add_skill_view, name='add_skill'),
    path('delete-skill/<int:skill_id>/', delete_skill_view, name='delete_skill'),
    path('register/', register_view, name='register'),
    path('', display_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('about/', about_view, name='about'),
    path('subscription/', subscription_view, name='subscription'),
    path('payment/<str:tier>/', payment_view, name='payment'),
    path('skills/', skills_view, name='skills'),
    path('add-skill/', add_skill_view, name='add_skill'),
    path('api/skills/', skill_api_list, name='skill-api'),
    path('admin/', admin.site.urls),
    path('', include('ledger.urls')),
    
]