from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
import pyttsx3 as p
import speech_recognition as sr
import requests
import json
from .models import Students
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import User
from .models import Notice
from .models import Roomate
from .models import Complaints
import razorpay
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


client = razorpay.Client(auth=('rzp_test_Uf40ViWrM2z7SJ', 'fU3dymHjBYgWR8dxVGTLQ4uk'))

def test_razorpay_connection(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        # Test API call to fetch orders (pagination with limit)
        response = client.order.all({'count': 1})
        return JsonResponse({'status': 'success', 'data': response})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# Create your views here.

def speak(message):
    engine = p.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', voice_id)
    engine.say(message)
    engine.runAndWait()

@login_required(login_url="/login_page/")
def Home(request):

    if request.method == "POST":
        # print('hello')
        command = request.POST.get('start-communication')
        # print(command)

        if command == 'start-communication':
            print('hello')
            engine = p.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate',rate)
            voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
            engine.setProperty('voice', voice_id)
            engine.say('Hello, I am your voice assistant. How can I help you?')
            engine.runAndWait()
            engine.say('what would you like to check')
            print('hello')
            engine.runAndWait()
            r=sr.Recognizer()

            with sr.Microphone() as source:
              r.energy_threshold=10000
              r.adjust_for_ambient_noise(source,1.2)
            #   print("Listening")
              audio=r.listen(source)
              text=r.recognize_google(audio)
              print(text)
            if text == 'check updates':
                return redirect('/updates/')
            elif text == 'roommate search':
                return redirect('/roomate_search/')
            elif text == 'fee payment':
                return redirect('/fee_payment/')
            elif text=='menu checking':
                return redirect('/menu_checking/')

            else:
                messages.error('request','unknown command')
                return redirect(' ')
    return render(request,'index.html')

@login_required(login_url="/login_page/")
def complains(request):

    if request.method == 'POST':
           data=request.POST
           room_number = data.get('room_number')
           complain = data.get('complain')
           if room_number and complain:
             Complaints.objects.create(room_number=room_number,complain=complain)
             return render(request,'complains.html') 
    else:
        return render(request,'complains.html') 
    
@login_required(login_url="/login_page/")
def complains_check(request):
    if request.user.username=='admin':
        notice=Complaints.objects.all()
        return render(request,'check_complains.html',context={'notices':notice})
    else:
        return redirect('/complain/')
      
    


@login_required(login_url="/login_page/")
def roomate_search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobilenumber = request.POST.get('number')
        if name and mobilenumber:
            Roomate.objects.create(name=name, mobilenumber=mobilenumber)
    
    # Fetch all roommates for both POST and GET requests
    peoples = Roomate.objects.all()
    return render(request, 'roomate_search.html', {'people': peoples})


@login_required(login_url="/login_page/")
def room_photos(request):
     return render(request,'room.html') 

@login_required(login_url="/login_page/")
def updates(request):
    if request.method == 'POST':
       username = request.user.username
       if username=='admin':
         return redirect('/update_form/') 
       else:
         notice=Notice.objects.all()
         return render(request,'updates.html',context={'notices':notice})
       
    else:
      notice=Notice.objects.all()
      return render(request,'updates.html',context={'notices':notice})
      #return render(request,'updates.html')
     #return render(request,'updates.html') 

@login_required(login_url="/login_page/")
def add_notice(request):
    if request.method =='POST':
        data=request.POST
        title = data.get('title')
        description = data.get('description')
        if title and description:
         notice=Notice(title=title,description=description)
         notice.save()
         return redirect('/updates/')
        else:
            return redirect('/updates/')
    return redirect('/updates/')

@login_required(login_url="/login_page/")
def delete_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            try:
                notice = Notice.objects.get(title=title)
                notice.delete()
            except Notice.DoesNotExist:
                # Optionally handle the case where the notice does not exist
                pass

        return redirect('updates')  # Use the named URL pattern for better maintainability

    return redirect('updates')  # Use the named URL pattern for better maintainability


@login_required(login_url="/login_page/")
def menu_checking(request):
    return render(request,'menu.html') 

@login_required(login_url="/login_page/")
def update_form(request):
   return render(request,'admin.html')
       
    

def login_page(request):
    if request.method=='POST':
        data = request.POST
        username = data.get('u')
        password = data.get('p')
        print(f"Username: {username}")
        print(f"Password: {password}")
        if not User.objects.filter(username=username).exists():
            messages.error(request,'user does not exist')
            return redirect('/login_page/')
        user = authenticate(request, username=username, password=password)
        print('hello')
        if user is not None:
            print('hello')
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'password is wrong')
            return redirect('/login_page/')
    return render(request,'login.html') 

def register(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('u')
        password=data.get('p')
        if  User.objects.filter(username=username).exists():
            messages.error(request,'user exists')
            return redirect('/register/')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.set_password(password)
            user.save()
            return redirect('/register/')
    return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login_page/')



            

            
               
            

            

        
        
        