from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from backend.permissions import NotAuthenticated
from backend.exceptions import AuthenticationFailed
from backend.serializers import RegistrationSerializer, LoginSerializer, ChangePasswordSerializer
from backend.models import User

__all__ = ['RegistrationView', 'LoginView', 'LogoutView', 'ChangePasswordView']

class RegistrationView(CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        # serialize request data
        data = request.data
        serializer = self.serializer_class(data = data)
        serializer.is_valid()
        
        user = serializer.save()
        # login the user
        login(request, user)
          
        messages.success(request, 'You have successfully registeed an account.')
        return Response({
            "status": "success", 
            "data": serializer.data,
        })
        
class LoginView(APIView):
    permission_classes = (NotAuthenticated, )
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self ,request):
        # serialize request data
        data = request.data
        serializer = self.serializer_class(data = data)
        serializer.is_valid()

        # authenticate user
        user = authenticate(**serializer.data)

        if not user:
            raise AuthenticationFailed({"detail": 'Invalid username and/or password.'})
        
        # login the user
        login(request, user)
        #generate token for user
        token, _ = Token.objects.get_or_create(user = user)
        # serialize data for display
        user_data = RegistrationSerializer(user).data

        return Response({
            "status": "success", 
            "data": {
                "user": user_data,
                "token": token.key
            }
        })
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        # delete current user token
        token = Token.objects.filter(user = user).delete()        
        # logout the current user
        logout(request)

        return Response({
            "status": "success", 
            "data": {
                "detail": 'You have been logged out successfully.',
            }
        })
    
class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)

        #authenticate again the user
        

        messages.success(request, "Password changed succesfully!")
        return Response({
            "status": "success", 
            "data": {
                "detail": 'Password changed succesfully!',
            }
        })







        
            