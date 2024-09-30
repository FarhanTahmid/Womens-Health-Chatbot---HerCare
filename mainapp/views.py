from django.shortcuts import render,redirect
from django.contrib import messages
from user.user_operations import UserOperations
# Create your views here.

def landingPage(request):
    
    if request.method=="POST":
        if(request.POST.get('login_button')):
            username=request.POST['username']
            password=request.POST['password']
            
            if(UserOperations.login(password=password,request=request,username=username)):
                print("User Logged in")
                return redirect('mainapp:landingPage')
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
                    return redirect('mainapp:landingPage')
                else:
                    print("You are already signed up. Try logging in instead!")
                    return redirect('mainapp:landingPage')

            else:
                print("Two Passwords didn't match")
                messages.info(request,"Two passwords didnt match")
                return redirect('mainapp:landingPage')
            
    return render(request,"landingpage.html")