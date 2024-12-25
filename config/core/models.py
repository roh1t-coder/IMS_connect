from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    role = models.CharField(max_length=255)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # Ensure unique constraint

class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)  # Set default value

    def __str__(self):
        return self.title

class Vote(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=255)

class Collaboration(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

class Reward(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward_type = models.CharField(max_length=255)