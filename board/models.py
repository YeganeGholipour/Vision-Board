from django.db import models
from user.models import User
from .choices import SubBoardStatusChoices, SubBoardPriorityChoices, RoleChoices

# Board
# Sub-Boards

# Goals
# Tasks



class Board(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubBoard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    inspiration = models.TextField()
    description = models.TextField()
    is_shared = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=20, 
        choices=SubBoardPriorityChoices.choices, 
        default=SubBoardPriorityChoices.MEDIUM,
        )
    status = models.CharField(
        max_length=20,
        choices=SubBoardStatusChoices.choices,
        default=SubBoardStatusChoices.PENDING,
    )

class SubBoardUser(models.Model):
    users = models.ManyToManyField(User, on_delete=models.CASCADE)
    sub_board = models.ForeignKey(SubBoard, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER)


class Goal(models.Model):  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    sub_board = models.ForeignKey(SubBoard, on_delete=models.CASCADE)  
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=20, 
        choices=SubBoardPriorityChoices.choices, 
        default=SubBoardPriorityChoices.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=SubBoardStatusChoices.choices,
        default=SubBoardStatusChoices.PENDING,
    )

class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=20, 
        choices=SubBoardPriorityChoices.choices, 
        default=SubBoardPriorityChoices.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=SubBoardStatusChoices.choices,
        default=SubBoardStatusChoices.PENDING,
    )
    assigned_to = models.ManyToManyField(User)  
