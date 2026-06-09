from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    # Link to the custom user model safely
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_swaps', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_swaps', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Pending') # Pending, Accepted, Completed
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} swapped {self.skill} with {self.receiver}"