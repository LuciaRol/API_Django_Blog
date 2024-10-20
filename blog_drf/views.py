# blog_drf/views.py

from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer

# REGISTER VIEW
class UserRegistrationView(generics.CreateAPIView):
    """Vista de API para el registro de usuarios."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Crear el usuario sin asignarlo a una variable
            return Response({"user": serializer.data, "message": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:  # Usando la ValidationError del módulo serializers
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        

# LOGIN VIEW
class UserLoginView(TokenObtainPairView):
    """API view for user login."""
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

