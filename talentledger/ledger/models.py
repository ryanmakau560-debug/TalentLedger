from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    # This refers to the standard, built-in Django User
    sender = models.ForeignKey(User, related_name='sent_swaps', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_swaps', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} swapped {self.skill} with {self.receiver}"