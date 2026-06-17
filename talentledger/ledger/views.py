from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SkillForm
from .models import Skill
from .models import Transaction
from django.contrib.auth.decorators import login_required

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