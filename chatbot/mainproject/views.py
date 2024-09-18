from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import google.generativeai as genai
import os
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
# client = OpenAI(api_key=openai_api_key) 
# Create your views here.

# openai_api_key= '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'

genai.configure(api_key="AIzaSyBYVl-gusTvysMXzjO8SyEmf9gXninEfbw")

# client = OpenAI(api_key=openai_api_key) 
def ask_openai(message):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(message).text
    return response



def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message = message, response = response, created_at = timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})    
    return render(request, 'chatbot.html', {'chats': chats})

# api key  = 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


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid Username or Password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password Incorrect'
            return render(request, 'register.html', {'error_message': error_message})
        
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

