from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('view-board/', views.ViewBoard.as_view(), name='view_board'),
    path('sub-board/<int:pk>/', views.ViewDetailSubBoard.as_view(), name='view_sub_board'),
    path('sub-board-users/<int:pk>/', views.SubBoardUserDetailView.as_view(), name='view_sub_board_users'),
    path('create-sub-board/', views.CreateSubBoard.as_view(), name='create_sub_board'),
    path('delete-sub-board/', views.DeleteSubBoard.as_view(), name='delete_sub_board'),
    path('update-sub-board/<int:pk>/', views.UpdateSubBoard.as_view(), name='update_sub_board'),  
    path('update-sub-board-user-access/<int:pk>/', views.UpdateUserAccessToSubBoard.as_view(), name='update_user_access'),  
]
