from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_skills')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_skills')

    def __str__(self):
        return self.name


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    study_credits = models.PositiveIntegerField(default=3)
    discord_username = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} ({self.study_credits} credits)"


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_swaps', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_swaps', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Pending')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    credit_awarded = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} swapped {self.skill} with {self.receiver}"