from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render,redirect
from user.models import ApplicationUser

class UserOperations:
    
    def login(username, password,request):
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return True
        else:
            print("Credentials given are wrong!")
            messages.error(request,"Credentials given are wrong")
            return False

    
    def signup(username, password, request):
        if(User.objects.filter(username=username).exists()):
            messages.info(request,"You are already signed up. Try logging in instead!")
            return False

        else:
            user=User.objects.create_user(username=username,password=password)
            user.save()
            new_user=ApplicationUser.objects.create(username=username)
            new_user.save()
            auth.login(request,user)
            return True
            
