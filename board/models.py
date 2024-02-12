from unicodedata import category
from django.db import models
from user.models import User
from .choices import SubBoardStatusChoices, SubBoardPriorityChoices, RoleChoices

# Board
# Sub-Boards

# Goals
# Tasks
# Category


class Board(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubBoard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='sub_boards')
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

    def __str__(self):
        return self.title

class SubBoardUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_board = models.ForeignKey(SubBoard, on_delete=models.CASCADE, related_name='sub_board')
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER)

    class Meta:
        unique_together = ('user', 'sub_board')

    # def save(self, *args, **kwargs):
    #     # On save, if this is the first user associated with the sub-board, designate them as admin
    #     if not self.sub_board.subboarduser_set.exists():
    #         self.role = RoleChoices.ADMIN
    #     super().save(*args, **kwargs)