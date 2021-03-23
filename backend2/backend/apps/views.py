from django.contrib.auth.models import User, Group
from rest_framework import permissions
from .serializers import UserSerializer
import json
from django.http import HttpResponse, JsonResponse
from .models import User
from rest_framework import status, viewsets, mixins 
from rest_framework.response import Response 
from django.views import View 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class viewSet(viewsets.ModelViewSet):
 
    
    serializer_class = UserSerializer
 
    # UserCreate
    def add(self, request): 
        musics = User.objects.filter(**request.data)
        if musics.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music_serializer = UserSerializer(data=request.data, partial=True)
        if not music_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music = music_serializer.save()

        return Response(UserSerializer(music).data, status=status.HTTP_200_CREATED)

    # # UserUpdate 
    def Userupdate(self, request): 
        return Response("수정완료", status=status.HTTP_201_CREATED)


    # UserDelete
    def Userdelete(self,request,user_seq): 
        deleteuser = User.objects.get(user_seq = user_seq)
        deleteuser.delete()
        return  Response("완료", status=status.HTTP_200_CREATED)



#로그아웃을 위한 api
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


      