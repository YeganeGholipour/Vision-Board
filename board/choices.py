from django.db import models

class SubBoardStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'


class SubBoardPriorityChoices(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM ='medium', 'Medium'
    HIGH = 'high', 'High'


class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'  # Can view, edit, delete board
    VIEWER = 'viewer', 'Viewer'  # Can view board
    USER = 'user', 'User'  # Can view, edit goals/tasks
