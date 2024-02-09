from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

from django.utils.http import urlsafe_base64_decode


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    confirm_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')
        username = data.get('username')

        if not username:
            raise serializers.ValidationError('Username is required')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')

        if not email:
            raise serializers.ValidationError('Email is required')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')

        if password and confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError('Passwords do not match')
        else:
            raise serializers.ValidationError('Password is required')

        return data


from rest_framework import serializers
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError('Username is required')

        if not password:
            raise serializers.ValidationError('Password is required')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data


class UserForgetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')

        if not email:
            raise serializers.ValidationError('Email is required')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exists')

        return data


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField() 

    def validate_uidb64(self, value):
        try:
            value = urlsafe_base64_decode(value)
            return value
        except (TypeError, ValueError):
            raise serializers.ValidationError('Invalid user ID.')
    


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid old password')
        return value
    
    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if not old_password:
            raise serializers.ValidationError('Old password is required')

        if not new_password:
            raise serializers.ValidationError('New password is required')

        if not confirm_new_password:
            raise serializers.ValidationError('Confirm new password is required')

        if new_password != confirm_new_password:
            raise serializers.ValidationError('Passwords do not match')
        
        return data
