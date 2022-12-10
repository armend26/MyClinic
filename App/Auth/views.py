from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from Doctors.models import Profile 

from .forms import CreateUserForm
from Doctors.forms import ProfileForm  


# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
        return redirect('complete')
    else:
        if request.method == 'POST':
            username = request.POST.get('username') 
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                if Profile.objects.filter(user=request.user,is_doctor=True).exists():
                    return redirect('doctorDashboard')
                return redirect('profileView')
            else:
                messages.info(request,'Check your username and password again!') 
    return render(request, 'Login/login.html') 



def registerView(request):

    if request.user.is_authenticated:
        return redirect('dashboardView')
    else:
        form = CreateUserForm() 

        if request.method == 'POST': 
            form = CreateUserForm(request.POST)
       
            if form.is_valid():
                user = form.save()   
                Profile.objects.create(user=user)
                user = form.cleaned_data.get('username') 
                messages.success(request, 'Thank you '+user+' for registering. Please login now to explore our app.  ')

                return redirect('loginView')
                 
    context = { 
        'form': form, 
         
    }
    return render(request,'Register/register.html',context) 
     

def logoutUser(request):
    logout(request)
    return redirect('loginView') 

 