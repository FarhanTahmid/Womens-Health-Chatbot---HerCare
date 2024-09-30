from django.shortcuts import render,redirect
from django.contrib import messages
from user.user_operations import UserOperations
from django.contrib.auth.decorators import login_required
from .models import UserConversationThreads
from user.models import ApplicationUser
from openai import OpenAI
import os
from .chatbot import Chatbot
from .context_generation import ContextGeneration
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# Create your views here.

def landingPage(request):
    
    if request.method=="POST":
        if(request.POST.get('login_button')):
            username=request.POST['username']
            password=request.POST['password']
            
            if(UserOperations.login(password=password,request=request,username=username)):
                print("User Logged in")
                return redirect('mainapp:chatbot')
            else:
                print("Credentials given are wrong")
                return redirect('mainapp:landingPage')


        if(request.POST.get('signup_button')):
            signupUsername=request.POST['signupUsername']
            signupPassword=request.POST['signupPassword']
            confirmPassword=request.POST['confirm_password']
            
            if(signupPassword==confirmPassword):
                print("Signing you up")
                if(UserOperations.signup(request=request,password=signupPassword,username=signupUsername)):
                    print("User Signed up and logged in")
                    return redirect('mainapp:chatbot')
                else:
                    print("You are already signed up. Try logging in instead!")
                    return redirect('mainapp:landingPage')

            else:
                print("Two Passwords didn't match")
                messages.info(request,"Two passwords didnt match")
                return redirect('mainapp:landingPage')
            
    return render(request,"landingpage.html")


class ChatbotAPI(APIView):    
    @permission_classes([IsAuthenticated])
    
    def get(self,request):
        # get username of the user
        username=request.user.username
        try:
            application_user=ApplicationUser.objects.get(username=username)
        except ApplicationUser.DoesNotExist:
            return redirect('mainapp:landingPage')
        
        if not request.user.is_authenticated:
            return Response({'msg': 'User is not authenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            previous_message_status,user_chat_list,assistant_chat_list,msg=Chatbot.getAllMessagesOfUser(userChoice=application_user.choice_of_convo_remembering,userobject=application_user)
            if(previous_message_status):
                return Response({'user_chat_list':user_chat_list,'assistant_chat_list':assistant_chat_list,'msg': msg}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': msg}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        # get username of the user
        username=request.user.username
        try:
            application_user=ApplicationUser.objects.get(username=username)
        except ApplicationUser.DoesNotExist:
            return redirect('mainapp:landingPage')
        
        if not request.user.is_authenticated:
            return Response({'msg': 'User is not authenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data=request.data
            user_message=data.get('user_message')
            
            bot_status,message=Chatbot.generateAssistantMessages(user_message=user_message,userchoice=application_user.choice_of_convo_remembering,userObject=application_user)
            
            if(bot_status):
                return Response({'msg':f"{message}"},status=status.HTTP_200_OK)
            else:
                print(message)
                return Response({'msg':f"{message}"},status=status.HTTP_400_BAD_REQUEST)



@login_required
def chatBox(request):
    username=request.user.username
    context={
        'username':username
    }
    return render(request,'chatBox.html',context=context)