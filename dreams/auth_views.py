from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import get_user_model, login

from .serializers import UserSerializer, LoginSerializer

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Validate password
                validate_password(serializer.validated_data['password'])
                
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "user": UserSerializer(user).data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response({"error": "weakPassword", "details": e.messages}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({"error": "userExists"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"error": "serverError"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if 'email' in serializer.errors:
                return Response({"error": "invalidEmail"}, status=status.HTTP_400_BAD_REQUEST)
            elif 'password' in serializer.errors:
                return Response({"error": "passwordMismatch"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data['usernameOrEmail']
            password = serializer.validated_data['password']

            try:
                # Try to fetch the user by username or email
                user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
                
                # Authenticate the user
                if user.check_password(password):
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "user": UserSerializer(user).data,
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    )
                else:
                    return Response(
                        {"error": "invalidCredentials"}, status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                # User not found
                return Response(
                    {"error": "invalidCredentials"}, status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                # Log the exception for debugging
                print(f"Unexpected error during login: {str(e)}")
                return Response(
                    {"error": "serverError"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)