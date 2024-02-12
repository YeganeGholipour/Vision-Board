from dataclasses import field
from rest_framework import serializers
from .models import Goal, Category, Task
from .choices import PriorityChoices, StatusChoices


class AddAndUpdateGoalToSubBoardSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=PriorityChoices.choices)
    status = serializers.ChoiceField(choices=StatusChoices.choices)
    category = serializers.StringRelatedField() # remove required=True
    class Meta:
        model = Goal
        field = ('title', 'description', 'due_date', 'priority', 'status', 'category')


class ListGoalsInSubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('title', 'due_date', 'priority', 'status')

class RetrieveGoalInASubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


class AddTaskToGoalSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField()
    goal = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta: 
        model = Task
        fields = ('title', 'description', 'due_date', 'priority', 'status', 'assigned_to', 'goal')
