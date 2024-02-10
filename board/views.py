from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .permissions import IsAdmin, IsViewer, IsUser, HasUserAcessToSubBoard, IsAdminOrIsUser
from .models import Board, SubBoard, SubBoardUser
from .serializers import ViewBoardSerializer, ViewDetailSubBoardSerializer, ViewDetailSubBoardUserSerializer, CreateSubBoardSerializer, UpdateSubBoardSerializer, UpdateUserAccessToSubBoardSerializer



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
    authentication_classes = [SessionAuthentication, TokenAuthentication]

class ViewDetailSubBoardUser(RetrieveAPIView):
    # views a single sub board that the user who has sent the request for
    # it also shows the name of the users who have access to this sub board
    serializer_class = ViewDetailSubBoardUserSerializer
    permission_classes = [IsAuthenticated, HasUserAcessToSubBoard]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

class CreateSubBoard(GenericAPIView, CreateModelMixin):
    serializer_class = CreateSubBoardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

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
    


    

