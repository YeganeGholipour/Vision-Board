from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from board.permissions import IsAdmin, IsAdminOrIsUser, HasUserAcessToSubBoard
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .serializers import (
    AddAndUpdateGoalToSubBoardSerializer, 
    ListGoalsInSubBoardSerializer, 
    RetrieveGoalInASubBoardSerializer,
    AddTaskToGoalSerializer
)

from .models import Goal
class AddGoalToSubBoardView(CreateAPIView):
    serializer_class = AddAndUpdateGoalToSubBoardSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class DeleteGoalFromSubBoardView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrIsUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class UpdateGoal(UpdateAPIView):
    serializer_class = AddAndUpdateGoalToSubBoardSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class ListGoalsInSubBoardView(ListAPIView):
    serializer_class = ListGoalsInSubBoardSerializer
    permission_classes = [IsAuthenticated, HasUserAcessToSubBoard]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, requst, *args, **kwargs):
        sub_board_id = kwargs.get('pk')
        goals = Goal.objects.filter(sub_board_id=sub_board_id)
        return goals

class RetrieveGoalInASubBoard(RetrieveAPIView):
    serializer_class = RetrieveGoalInASubBoardSerializer
    permission_classes = [IsAuthenticated, HasUserAcessToSubBoard]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class AddTaskToGoal(CreateAPIView):
    serializer_class = AddTaskToGoalSerializer
    permission_class = [IsAuthenticated, IsAdminOrIsUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class DeleteTaskFromGoal(DestroyAPIView):
    permission_class = [IsAuthenticated, IsAdminOrIsUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


