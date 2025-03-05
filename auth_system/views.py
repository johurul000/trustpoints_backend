from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import AppUser
from .serializers import AppUserSerializer, SimpleRegistrationSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AppUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SimpleRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'points': user.points,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class EditUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', request.user.id)  # Default to self if no user_id

        # Allow users to edit only their own profile, unless they are admins
        if request.user.id != user_id and not request.user.is_admin:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(AppUser, id=user_id)
        serializer = AppUserSerializer(user, data=request.data, partial=True)  # Partial updates allowed
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Admin Logic


class GetAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Ensure the user is an admin
        if not user.is_admin:
            return Response({"error": "Unauthorized: Admin access required"}, status=status.HTTP_403_FORBIDDEN)

        # Serialize and return admin data
        serializer = AppUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user and user.is_admin:  # Check if the user is an admin
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            access_token["role"] = user.role
            access_token["user_id"] = user.id
            access_token["email"] = user.email

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(access_token),  # Convert token to string
                    "admin": True,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials or not an admin"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
class EditAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        admin_id = kwargs.get("admin_id", request.user.id)  # Default to self if no admin_id

        # Allow only admins to edit their profile or other admins
        if not request.user.is_admin:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(AppUser, id=admin_id, is_admin=True)  # Ensure the user is an admin
        serializer = AppUserSerializer(user, data=request.data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer



