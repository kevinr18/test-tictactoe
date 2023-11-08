from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


# Create your views here.
class UserCreate(APIView):
    permission_classes = [AllowAny]
    """
        Permite crear usuarios o jugadores para la aplicación
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'message': 'Nombre de usuario y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'message': 'Nombre de usuario ya existe'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    

class UserLogin(APIView):
    permission_classes = [AllowAny]
    """
        Permite conectarse a la aplicacion con un usuario 
        previamente creado y obtener un token.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Nombre de usuario y contraseña son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user != None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogout(APIView):
    """
        Elimina el token asociado al usuario.
    """
    def get(self, request):
        user = request.user
        user.auth_token.delete()
        return Response(
            {'message': "Cierre de sesión exitoso. El token ha sido eliminado."}
        )