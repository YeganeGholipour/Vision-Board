from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .models import User
from board.models import Board

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserForgetPasswordRequestSerializer, UserPasswordResetConfirmSerializer, UserChangePasswordSerializer
class RegisterView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        board = Board.objects.create(user=user)
        board.save()

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



class ChangePasswordView(APIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Check if the old password matches the user's current password
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and save the user object
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)




class ForgetPasswordRequestView(APIView):
    serializer_class = UserForgetPasswordRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        # Generate a token for the user
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Build the reset URL
        reset_link = reverse('password_reset_confirm', args=[user.pk, token])
        reset_url = request.build_absolute_uri(reset_link)

        # Send the password reset email to the user
        subject = 'Password Reset Request'
        message = f'Hello,\n\nYou have requested to reset your password. Please click on the following link to reset your password:\n\n{reset_url}\n\nIf you did not request this, please ignore this email.\n\nThank you.\n'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)

    

class PasswordResetConfirmView(APIView):
    serializer_class = UserPasswordResetConfirmSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


