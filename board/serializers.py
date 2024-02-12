from dataclasses import fields
from rest_framework import serializers
from .models import Board, SubBoard, SubBoardUser
from user.models import User
from .choices import SubBoardStatusChoices, SubBoardPriorityChoices, RoleChoices

class ViewBoardSerializer(serializers.ModelSerializer):
    sub_board = serializers.StringRelatedField()
    class Meta:
        model = Board
        fields = ('created_at', 'updated_at', 'sub_board')


class SubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBoard
        fields = ('id', 'created_at', 'updated_at', 'title', 'inspiration', 'description', 'is_shared', 'due_date', 'priority','status')


class ViewDetailSubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBoard
        fields = ('id', 'created_at', 'updated_at', 'title', 'inspiration', 'description', 'is_shared', 'due_date', 'priority','status')


class UserSubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'profile_pic')

class ViewDetailSubBoardUserSerializer(serializers.ModelSerializer):
    sub_board = SubBoardSerializer()
    users = serializers.StringRelatedField()
    class Meta:
        model = SubBoardUser
        fields = ('users','sub_board', 'join_date', 'role')


class CreateSubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBoard
        fields = ('title', 'inspiration', 'description', 'is_shared', 'due_date', 'priority','status')

    def create(self, validated_data):
        # Get the board instance from the serializer context
        board = self.context.get('board')
        # Set the board field of the sub-board
        validated_data['board'] = board
        # Create and return the sub-board instance
        return super().create(validated_data)


class AddUsersToSubBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBoardUser
        fields = ('users', 'role')


class UpdateSubBoardSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=SubBoardPriorityChoices)
    status = serializers.ChoiceField(choices=SubBoardStatusChoices)
    class Meta:
        model = SubBoard
        fields = ['title', 'inspiration', 'description', 'is_shared', 'due_date', 'priority', 'status']


class UpdateUserAccessToSubBoardSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField()  
    role = serializers.ChoiceField(choices=RoleChoices.choices)
    class Meta:
        model = SubBoardUser
        fields = ('users', 'role')

class SubBoardUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) #////
    sub_board = serializers.PrimaryKeyRelatedField(queryset=SubBoard.objects.all()) #/////
    role = serializers.ChoiceField(choices=RoleChoices.choices)
    class Meta:
        model = SubBoardUser
        fields = ('user', 'role', 'sub_board')