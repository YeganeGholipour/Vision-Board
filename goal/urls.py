from django.urls import path
from . import views

app_name = 'goal'

urlpatterns = [
    path('add-goal/<int:pk>/', views.AddGoalToSubBoardView.as_view(), name='add_goal_to_subboard'),
    path('delete-goal/<int:pk>', views.DeleteGoalFromSubBoardView.as_view(), name="delete_goal_from_subboard"),
    path('update-goal/<int:sub_board_pk>/<int:goal_pk>/', views.UpdateGoal.as_view(), name='update_goal'),
    path('list-goals/<int:pk>/', views.ListGoalsInSubBoardView.as_view(), name='list_goals'),
    path('retrieve-goal/<int:sub_board_pk>/<int:goal_pk>/', views.RetrieveGoalInASubBoard.as_view(), name='retrieve_goal'),
    path('add-task/<int:sub_board_pk>/<int:goal_pk>/', views.AddTaskToGoal.as_view(), name='add_task'),
    path('delete-task/<int:sub_board_pk>/<int:goal_pk>/<int:task_pk>/', views.DeleteTaskFromGoal.as_view(), name="delete_task"),
]
