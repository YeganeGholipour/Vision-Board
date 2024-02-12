from django.db import models
from board.models import SubBoard
from .choices import StatusChoices, PriorityChoices
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Goal(models.Model):  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    sub_board = models.ForeignKey(SubBoard, on_delete=models.CASCADE, related_name='goals')  
    due_date = models.DateTimeField(null=True)
    category = models.ManyToManyField(Category, related_name="goal_categories")
    priority = models.CharField(
        max_length=20, 
        choices=PriorityChoices.choices, 
        default=PriorityChoices.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    def __str__(self):
        return self.title 

class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True)
    priority = models.CharField(
        max_length=20, 
        choices=PriorityChoices.choices, 
        default=PriorityChoices.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    assigned_to = models.ManyToManyField(User)  

    def __str__(self):
        return self.title