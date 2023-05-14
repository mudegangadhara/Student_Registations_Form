from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def Registation(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            NUFD=UFD.save(commit=False)
            NUFD.set_password(UFD.cleaned_data['password'])
            NUFD.save()
            NPFD=PFD.save(commit=False)
            NPFD.username=NUFD
            NPFD.save()
            send_mail('Registations'," Registation is succcessfully",'mudegangadharanaik113@gmail.com',[NUFD.email],fail_silently=False)
            return HttpResponse('Registation is successfully.......')
        else:
            return HttpResponse('IN Valid Data')
    return render(request,'Registation.html',d)


def home(request):
    if request.session.get('username'):
        user=request.session.get('username')
        D={'username':user}
        return render(request,'home.html',D)
    return render(request,'home.html')




def user_Login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username, password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    
    d={'UO':UO}   
    return render(request,'display_profile.html',d)

def Forgot_password(request):
    if request.method == 'POST':
        
        UD=request.POST.get('un')
        PW=request.POST.get('ps')
        LUO=User.objects.filter(username=UD)
        if LUO:
            UO=LUO[0]
            UO.set_password(PW)
            UO.save()
            return HttpResponse('Password is Changed')
        else:
            return HttpResponse('User Name Is Not In DataBase')
    return render(request,'f_w.html')