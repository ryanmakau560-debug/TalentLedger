from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SkillForm
from .models import Skill
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Skill
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Skill
from .serializers import SkillSerializer
from rest_framework import status
@api_view(['PUT', 'DELETE'])
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    if request.method == 'PUT':
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST'])
def skill_api_list(request):
    if request.method == 'GET':
        category = request.query_params.get('category', None)
        if category:
            skills = Skill.objects.filter(category=category)
        else:
            skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
@login_required
def profile_view(request):
    user_skills = Skill.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_skills': user_skills})

def contact_view(request):
    return render(request, 'contact.html')

def get_user_credits(user):
    user_skills = Skill.objects.filter(user=user)
    return sum(skill.credits for skill in user_skills)
def skills_view(request):
    skills = Skill.objects.all() 
    return render(request, 'skills.html', {'skills': skills})
@login_required
def add_skill_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        credits = request.POST.get('credits')
        # This saves the skill linked to the current logged-in user
        Skill.objects.create(user=request.user, name=name, credits=credits)
        return redirect('skills') 
    return render(request, 'add_skill.html')

def add_skill_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        credits = request.POST.get('credits')
        # Saves the skill linked to the logged-in user
        Skill.objects.create(user=request.user, name=name, credits=credits)
        return redirect('skills') # Redirects to the list page
    return render(request, 'add_skill.html')
def payment_view(request, tier):
    return render(request, 'payment.html', {'tier': tier})
def subscription_view(request):
    return render(request, 'subscription.html')
def display_view(request):
    return render(request, 'display.html')

def about_view(request):
    return render(request, 'about.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def delete_skill_view(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    if request.method == 'POST':
        skill.delete()
    return redirect('dashboard')

@login_required
def add_skill_view(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user # Link the skill to the logged-in user
            skill.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    
    return render(request, 'add_skill.html', {'form': form})

@login_required
def dashboard_view(request):
    user_skills = Skill.objects.filter(user=request.user) 
    return render(request, 'pages/dashboard.html', {'skills': user_skills})
@login_required
def profile_view(request):
    return render(request, 'profile.html') # You'll need to create this template
def request_swap(request, skill_id):
    # This is a simplified logic for now
    skill = Skill.objects.get(id=skill_id)
    if request.method == 'POST':
        # Create a new transaction in the ledger
        Transaction.objects.create(
            sender=request.user,
            skill=skill,
            hours=request.POST.get('hours'),
            status='Pending'
        )
        return redirect('marketplace')
@csrf_exempt
def dashboard(request):
    # This filters transactions to show only those involving the current user
    user_swaps = Transaction.objects.filter(sender=request.user)
    return render(request, 'pages/dashboard.html', {'swaps': user_swaps})
def test_postman(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Success! Django is talking to Postman."})

from django.shortcuts import render

def home(request):

    return render(request, 'pages/home.html')
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SkillForm()
    return render(request, 'pages/add_skill.html', {'form': form})
def marketplace(request):
    skills = Skill.objects.all()
    return render(request, 'pages/marketplace.html', {'skills': skills})
