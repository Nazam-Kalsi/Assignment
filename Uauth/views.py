from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .serializer import UserRegistrationSerializer, UserLoginSerializer
from .models import customUser
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(generics.CreateAPIView):
    queryset = customUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print(user)
            try:
                 token = Token.objects.get(user=customUser)  # Try to retrieve existing token
            except Token.DoesNotExist:
                 token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)  
    

class GetUserDetailsView(generics.GenericAPIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'userInfo': {
                    'id': request.user.id,
                    'email': request.user.email,
                    'username': request.user.username
                }
            })
        return Response({'error': 'User is not authenticated'}, status=400)
    



