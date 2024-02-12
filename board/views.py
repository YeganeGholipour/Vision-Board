from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .permissions import IsAdmin, IsViewer, IsUser, HasUserAcessToSubBoard, IsAdminOrIsUser
from .models import Board, SubBoard, SubBoardUser
from .serializers import (
    ViewBoardSerializer, ViewDetailSubBoardSerializer, 
    ViewDetailSubBoardUserSerializer, CreateSubBoardSerializer, 
    UpdateSubBoardSerializer, UpdateUserAccessToSubBoardSerializer,
    SubBoardUserSerializer,
    )



class ViewBoard(ListAPIView):
    # Basically views all the sub boards in the board
    serializer_class = ViewBoardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Board.objects.filter(user=user)
        return queryset

class ViewDetailSubBoard(RetrieveAPIView):
    # views a single sub board that the user who has sent the request for
    # the user needs to be in the list of users who have access to the board -> HasUserAcessToSubBoard Permission
    serializer_class = ViewDetailSubBoardSerializer
    permission_classes = [IsAuthenticated, HasUserAcessToSubBoard]
    # permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        # Retrieve the pk from the URL kwargs
        pk = self.kwargs.get('pk')
        # Filter the queryset to get the SubBoard with the specified pk
        queryset = SubBoard.objects.filter(pk=pk)
        return queryset
    

class SubBoardUserDetailView(RetrieveAPIView):
    serializer_class = SubBoardUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = SubBoardUser.objects.all()  # Start with all SubBoardUser instances

    def get(self, request, *args, **kwargs):
        sub_board_id = kwargs.get('pk')  # Get the sub_board_id from URL params
        sub_board_users = SubBoardUser.objects.filter(sub_board_id=sub_board_id)  # Filter SubBoardUser instances based on sub_board_id
        serializer = self.get_serializer(sub_board_users, many=True)
        return Response(serializer.data)


class CreateSubBoard(GenericAPIView, CreateModelMixin):
    serializer_class = CreateSubBoardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request, *args, **kwargs):

        # Get the current user's board
        user = request.user
        board = Board.objects.get(user=user)

        serializer = self.get_serializer(data=request.data, context={'board': board})
        serializer.is_valid(raise_exception=True)

        # creates the sub board instance
        sub_board_inst = serializer.save()

        # sub board user instance
        sub_board_user_data = {
            "sub_board": sub_board_inst.pk,
            "user": request.user.pk,
            "role": "admin",
        }
        
        sub_board_user_serializer = SubBoardUserSerializer(data=sub_board_user_data)
        sub_board_user_serializer.is_valid(raise_exception=True)

        # creates the sub board user instance
        sub_board_user_inst = sub_board_user_serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DeleteSubBoard(GenericAPIView, DestroyModelMixin):
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class UpdateSubBoard(GenericAPIView,UpdateModelMixin): 
    serializer_class = UpdateSubBoardSerializer 
    permission_classes = [IsAuthenticated, IsAdminOrIsUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UpdateUserAccessToSubBoard(GenericAPIView, UpdateModelMixin): 
    serializer_class = UpdateUserAccessToSubBoardSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    


    

