from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework import status as drf_status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CustomUserCreationForm, SkillForm
from .models import Session, Skill, Transaction, UserProfile
from .serializers import SkillSerializer


# --- Template / Page Views ---

def home(request):
    return render(request, 'home.html')


def display_view(request):
    return render(request, 'display.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def subscription_view(request):
    return render(request, 'subscription.html')


def payment_view(request, tier):
    return render(request, 'payment.html', {'tier': tier})


def skills_view(request):
    skills = Skill.objects.all()
    return render(request, 'skills.html', {'skills': skills})


def marketplace(request):
    skills = Skill.objects.all()
    return render(request, 'marketplace.html', {'skills': skills})


@login_required
def add_skill_view(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            if hasattr(skill, 'user'):
                skill.user = request.user
            if hasattr(skill, 'instructor') and not skill.instructor_id:
                skill.instructor = request.user
            skill.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})


@csrf_exempt
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})


@login_required
def delete_skill_view(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    if request.method == 'POST':
        skill.delete()
    return redirect('dashboard')


@login_required
def profile_view(request):
    user_skills = Skill.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_skills': user_skills})


@csrf_exempt
def dashboard(request):
    user_swaps = Transaction.objects.filter(sender=request.user) if request.user.is_authenticated else Transaction.objects.none()
    return render(request, 'dashboard.html', {'swaps': user_swaps})


@csrf_exempt
def dashboard_view(request):
    user_skills = Skill.objects.filter(user=request.user) if request.user.is_authenticated else Skill.objects.none()
    my_transactions = Transaction.objects.filter(sender=request.user) if request.user.is_authenticated else Transaction.objects.none()
    return render(request, 'dashboard.html', {
        'my_transactions': my_transactions,
        'skills': user_skills,
    })


@login_required
def received_requests_view(request):
    requests = Transaction.objects.filter(
        skill__instructor=request.user,
        status__iexact='pending'
    )
    return render(request, 'received_requests.html', {'requests': requests})

@method_decorator(csrf_exempt, name='dispatch')
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class MyLoginView(LoginView):
    pass


# --- Action / Helper Views ---

def get_user_credits(user):
    user_skills = Skill.objects.filter(user=user)
    return sum(skill.credits for skill in user_skills)


@require_POST
@csrf_exempt
def toggle_book_session(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    existing = Transaction.objects.filter(sender=request.user, skill=skill).first()

    if existing:
        existing.delete()
    else:
        Transaction.objects.create(
            sender=request.user,
            receiver=skill.user,
            skill=skill,
            hours=1,
            status='Pending',
        )

    return redirect('dashboard')


@require_POST
@csrf_exempt
def update_transaction_status(request, transaction_id, action):
    tx = get_object_or_404(Transaction, id=transaction_id)
    if action == 'accept':
        tx.status = 'confirmed'
    elif action == 'reject':
        tx.status = 'rejected'
    tx.save()
    return redirect('dashboard')


def request_swap(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == 'POST':
        Transaction.objects.create(
            sender=request.user,
            skill=skill,
            hours=request.POST.get('hours'),
            status='Pending',
        )
        return redirect('marketplace')
    return redirect('marketplace')


def test_postman(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Success! Django is talking to Postman."})


def _serialize_transaction(tx):
    return {
        "id": tx.id,
        "skill_id": tx.skill.id,
        "skill_name": tx.skill.name,
        "category": tx.skill.category,
        "learner_id": tx.sender.id,
        "learner_username": tx.sender.username,
        "instructor_id": tx.skill.instructor.id,
        "instructor_username": tx.skill.instructor.username,
        "hours": tx.hours,
        "status": tx.status,
        "scheduled_time": tx.scheduled_time.isoformat() if tx.scheduled_time else None,
        "timestamp": tx.timestamp.isoformat(),
    }


# --- API Views ---

@csrf_exempt
def list_users(request):
    users_data = []
    for u in User.objects.all():
        profile, _ = UserProfile.objects.get_or_create(user=u)
        users_data.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'study_credits': profile.study_credits,
        })
    return JsonResponse({'users': users_data}, safe=False)


@api_view(['GET', 'POST'])
@csrf_exempt
def skill_api_list(request):
    if request.method == 'GET':
        category = request.query_params.get('category', None)
        skills = Skill.objects.filter(category=category) if category else Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    serializer = SkillSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)

    if request.method == 'PUT':
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    skill.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(["POST"])
def set_user_password(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Both username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    user.set_password(password)
    user.save()
    UserProfile.objects.get_or_create(user=user)

    return Response(
        {"message": f"Password set for {user.username}."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def simple_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    profile, _ = UserProfile.objects.get_or_create(user=user)

    return Response(
        {
            "message": "Logged in successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "study_credits": profile.study_credits,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def simple_signup(request):
    username = (request.data.get("username") or "").strip()
    password = request.data.get("password") or ""

    if not username or not password:
        return Response(
            {"error": "Both username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, password=password)
    profile, _ = UserProfile.objects.get_or_create(user=user)

    return Response(
        {
            "message": "Account created successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "study_credits": profile.study_credits,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@csrf_exempt
@api_view(['POST'])
def api_book_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    learner_id = request.data.get("user_id") or request.data.get("sender_id")
    hours = int(request.data.get("hours", 1))

    if hours <= 0:
        return Response({"error": "hours must be greater than 0"}, status=drf_status.HTTP_400_BAD_REQUEST)

    if learner_id:
        learner = get_object_or_404(User, id=int(learner_id))
    elif request.user.is_authenticated:
        learner = request.user
    else:
        return Response({"error": "Provide user_id in JSON body"}, status=drf_status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        profile, _ = UserProfile.objects.select_for_update().get_or_create(user=learner)

        if profile.study_credits < hours:
            return Response(
                {
                    "error": "Insufficient study credits to book this session.",
                    "available_credits": profile.study_credits,
                    "required_hours": hours,
                },
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        profile.study_credits -= hours
        profile.save()

        tx = Transaction.objects.create(
            sender=learner,
            receiver=skill.instructor,
            skill=skill,
            hours=hours,
            status="Pending",
        )

    return Response(_serialize_transaction(tx), status=drf_status.HTTP_201_CREATED)


@api_view(['GET'])
def api_instructor_requests(request):
    instructor_id = request.query_params.get("instructor_id") or request.query_params.get("user_id")
    if instructor_id:
        qs = Transaction.objects.filter(skill__instructor_id=int(instructor_id))
    elif request.user.is_authenticated:
        qs = Transaction.objects.filter(skill__instructor=request.user)
    else:
        qs = Transaction.objects.all()

    status_filter = request.query_params.get("status")
    if status_filter:
        qs = qs.filter(status__iexact=status_filter)

    qs = qs.order_by("-timestamp")
    return Response([_serialize_transaction(tx) for tx in qs], status=drf_status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST', 'PATCH', 'PUT'])
def api_respond_booking(request, transaction_id):
    tx = get_object_or_404(Transaction, id=transaction_id)
    action = (request.data.get("action") or request.data.get("status") or "accept").lower()
    raw_time = request.data.get("scheduled_time")

    if action in ("accept", "accepted", "confirm", "confirmed"):
        tx.status = "confirmed"
        if raw_time:
            parsed = parse_datetime(str(raw_time))
            if not parsed:
                return Response(
                    {"error": "Invalid scheduled_time. Use ISO format like 2026-11-28T15:00:00Z"},
                    status=drf_status.HTTP_400_BAD_REQUEST,
                )
            tx.scheduled_time = parsed
    elif action in ("reject", "rejected", "decline", "declined"):
        tx.status = "rejected"
    else:
        return Response({"error": "action must be 'accept' or 'reject'"}, status=drf_status.HTTP_400_BAD_REQUEST)

    tx.save()
    return Response(_serialize_transaction(tx), status=drf_status.HTTP_200_OK)


@api_view(['GET'])
def api_my_bookings(request):
    learner_id = request.query_params.get("user_id") or request.query_params.get("sender_id")
    if learner_id:
        qs = Transaction.objects.filter(sender_id=int(learner_id))
    elif request.user.is_authenticated:
        qs = Transaction.objects.filter(sender=request.user)
    else:
        qs = Transaction.objects.all()

    qs = qs.order_by("-timestamp")
    return Response([_serialize_transaction(tx) for tx in qs], status=drf_status.HTTP_200_OK)


@api_view(['POST'])
def award_booking_credit(request, pk):
    with transaction.atomic():
        tx = get_object_or_404(
            Transaction.objects.select_for_update().select_related('skill__instructor', 'receiver'),
            pk=pk,
        )

        if tx.status.lower() != 'confirmed':
            return Response(
                {'error': f"Cannot award credits for a booking with status '{tx.status}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if tx.credit_awarded:
            return Response(
                {'error': 'Credits have already been awarded for this session.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tutor = tx.skill.instructor or tx.receiver
        profile, _ = UserProfile.objects.get_or_create(user=tutor)
        profile.study_credits += tx.hours
        profile.save()

        tx.credit_awarded = True
        tx.save()

    return Response(
        {
            'message': 'Study credits awarded.',
            'transaction_id': tx.id,
            'tutor_id': tutor.id,
            'tutor_username': tutor.username,
            'hours_awarded': tx.hours,
            'study_credits': profile.study_credits,
        },
        status=status.HTTP_200_OK,
    )