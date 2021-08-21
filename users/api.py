from rest_framework import generics, permissions, views as rview, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer
import os, subprocess
from django.contrib.auth.models import User

# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if self.request.user.id:  
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
    else:
      return Response({"error":"Authentication of the registrar is invalid"})
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })

# Login API
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token,
      'expiry': _.expiry.timestamp()
    })

# Get User API
class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user

  
  

class UpdatePassword(rview.APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.get('profile', False):
          return self.change_other_details()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'message':"Successfully changed the password"},status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def change_other_details(self):
      
      for x,y in self.request.data.items():
        if x == 'password':
          continue
        else:
          self.object.__setattr__(x,y)
      self.object.save()
      return Response({'user':UserSerializer(instance = self.object).data}, status=status.HTTP_200_OK)
  
# class CheckTokenExpTime(rview.APIView):
#   def get_permissions(self):
#     return [permissions.IsAuthenticated(),]

#   def get(self,request):
#     AuthToken.objects.get()
  
    

class Pull(rview.APIView):
  def get_permissions(self):
    return [permissions.IsAdminUser(),]
  
  def get(self, request):
    cwd = os.getcwd()
    # os.chdir("/home/ppc/deploy/GandakiProvinceFrontEnd")
    # subprocess.run(['ls'])
    # subprocess.run(["git", "pull"])
    os.chdir("/home/ppc/deploy/GandakiProvinceData/server/configs/")
    if request.GET.get('restart', False):
      subprocess.run("./restart_portal.sh")
      return Response({"message":"Successfully Restarted the System"}, status = 200)
    else:
      os.chdir("/home/ppc/deploy/GandakiProvinceData")
      subprocess.run(["git", "pull"])
      # subprocess.run("./pull.sh")
      os.chdir("/home/ppc/deploy/GandakiProvinceFrontEnd")
      subprocess.run(["git", "pull"])
      os.chdir("/home/ppc/deploy/NewFrontEndGandakiProvinceData")
      subprocess.run(["git", "pull"])

      return Response({"message":"Successfully Pulled FrontEnd and BackEnd", "next-step":"To restart system send GET paramenters \"restart\":true"}, status = 200)
    
    
    