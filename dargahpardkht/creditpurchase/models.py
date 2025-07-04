from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    credits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.credits} credits"
