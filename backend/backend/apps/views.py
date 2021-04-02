from django.contrib.auth.models import User, Group
from rest_framework import permissions
from .serializers import *
from .models import User
from rest_framework import status, viewsets, mixins 
from rest_framework.response import Response 
from django.views import View 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
#이메일 인증을 위해 추가로 import 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .text import message



@permission_classes([AllowAny])
class UserViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,View): 

    serializer_class = UserSerializer				

    def login(self, request, email, password):
         
        loginUser =  User.objects.filter(email =email , password = password)
        
        if loginUser.exists():
            request.session['email'] = email
            serializer = UserSerializer(loginUser, many=True) 
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def sessionCheck(self, request):
        
        userSession = request.session.get('email')
        
        if userSession :
            user = User.objects.get(email = userSession)
            return Response(user.email,status=status.HTTP_200_OK)
       
        return Response("로그인 필요",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def logout(self, request):
        
        del request.session['email']
        return Response("로그 아웃",status=status.HTTP_200_OK)
        
    def signUp(self, request): 
        #회원가입 시 
        users =  User.objects.filter(email =request.data["email"])

        if users.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        userSerializer = UserSerializer(data=request.data, partial=True)
        if not userSerializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        userSerializer.save()
        print(users.seq)
        current_site = get_current_site(request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(users.seq))
        message_data = message(domain, uidb64)
        mail_title = "이메일 인증을 완료해주세요"
        mail_to = data['email']
        email = EmailMessage(mail_title, message_data, to=[mail_to])
        email.send()

        return Response("회원가입완료", status=status.HTTP_201_CREATED)


    def userInfoUpdate(self,request, email):

        users =  User.objects.filter(email =email)
        if not users.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        userInfoModify = User.objects.get(email=email)
        userInfoModify.password = request.data["password"]
        userInfoModify.baek_id  = request.data["baek_id"]
        userInfoModify.nickname = request.data["nickname"]
        userInfoModify.profile_image = request.data["profile_image"]
        userInfoModify.save()

        return Response("수정 성공",status=status.HTTP_200_OK)

    def Userdelete(self,request,email): 
        
        users = User.objects.filter(email = email)
        if not users.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
       
        users.delete()
        
        return  Response("삭제성공", status=status.HTTP_200_OK)
    
    #이메일 인증
    def get(self, request, uidb64, seq, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=seq)
            # user_dic = jwt.decode(token,SECRET_KEY,algorithm='HS256')
            if user.seq == user_dic["user"]:
                user.is_active = True
                user.save()  
                return "아주 잘 됨"

            return JsonResponse({'message':'auth fail'}, status=400)
        except ValidationError:
            return JsonResponse({'message':'type_error'}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)

@permission_classes([AllowAny])
class Activate(View):
    def get(self, request, uidb64, token):
        try:
            # uid = force_text(urlsafe_base64_decode(uidb64))
            # user = Users.objects.get(pk=seq)
            # if user.id == user_dic["user"]:
            #     user.is_active = True
            #     user.save()
            #     return "완료"

            return "완료"
            # return JsonResponse({'message':'auth fail'}, status=400)
        except ValidationError:
            return JsonResponse({'message':'type_error'}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)


@permission_classes([AllowAny])
class codeBoardViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,View):
    
    serializer_class = CodeBoardSerializer
   
    def codeBoardAll(self, request):

        boardcodes = CodeBoard.objects.all()
        serializer = CodeBoardSerializer(boardcodes, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def codeBoardPage(self, request , codeBoard_seq):
       
        codeBoard =  CodeBoard.objects.filter(seq =codeBoard_seq)
        if not codeBoard.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CodeBoardSerializer(codeBoard, many=True)    

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def codeBoardRegiste(self, request):
        
        codeBoardSerializer = CodeBoardSerializer(data=request.data, partial=True)
        if not codeBoardSerializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        codeBoardSerializer.save()

        return Response("코드보드 등록완료", status=status.HTTP_201_CREATED)
    
    def codeBoardUpdate(self, request, codeBoard_seq):
        
        codeBoard =  CodeBoard.objects.filter(seq =codeBoard_seq)
        if not codeBoard.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        codeBoard.update(code =request.data["code"],explanation  =request.data["explanation"],free_write =request.data["free_write"],problem_seq=request.data["problem_seq"],language_seq=request.data["language_seq"])
        return Response("수정 성공",status=status.HTTP_200_OK)


    def codeBoardDelete(self, request, codeBoard_seq):

        codeBoard =  CodeBoard.objects.filter(seq =codeBoard_seq)
        if not codeBoard.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        codeBoard.delete()
        
        return  Response("삭제성공", status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class commentViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,View):

    serializer_class = CommentSerializer

    def commentRegiste(self, request):

        commentSerializer = CommentSerializer(data=request.data, partial=True)
        if not commentSerializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        commentSerializer.save()


        return  Response("댓글등록", status=status.HTTP_201_CREATED)   

    def commentUpdate(self, request, comment_seq):
        
        comment =  Comment.objects.filter(seq =comment_seq)
        if not comment.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        comment.update(text =request.data["text"])
        return Response("수정 성공",status=status.HTTP_200_OK)
    
    def commentDelete(self, request, comment_seq):

        comment =  Comment.objects.filter(seq =comment_seq)
        if not comment.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        comment.delete()
        
        return  Response("삭제성공", status=status.HTTP_200_OK)
    
    def commentList(self, request , codeBoard_seq):
       
        comments =  Comment.objects.filter(code_board_seq = codeBoard_seq)
        if not comments.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CommentSerializer(comments, many=True)    

        return Response(serializer.data, status=status.HTTP_200_OK)
      