from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from Doctors.models import Doctor,Appointment,Profile
from Doctors.forms import AppointmentForm,ProfileForm
from django.contrib import messages 
from django.db.models import Count
from .datelist import getDateList
from .timeslot import timeslot
from .excelReport import createReport
from openpyxl import Workbook 
from openpyxl.writer.excel import save_virtual_workbook
from django.db import IntegrityError

# Create your views here.
@login_required(login_url='loginView')
def dashboardView(request):
    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete')

    if Profile.objects.filter(user=request.user,is_doctor=True).exists():
        return HttpResponse("Please go back,this page it's only for user's.")

    return render(request, 'Dashboard/dashboard.html') 


@login_required(login_url='loginView')
def profileView(request): 
    context = { } 
    #doctor_login 
   

    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete')
    
    if Profile.objects.filter(user=request.user,is_doctor=True).exists():
        return redirect('doctorDashboard')

    context["dataset"] = Profile.objects.filter(user=request.user)

    return render(request, 'Dashboard/profile.html',context)  


@login_required(login_url='loginView') 
def doctorView(request):
    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete') 
    
    if Profile.objects.filter(user=request.user,is_doctor=True).exists():
        return HttpResponse("Please go back,this page it's only for user's.")

    doctor = Doctor.objects.filter(id=request.user.profile.doctor.id) 

    appointment = Appointment.objects.filter(doctor=request.user.profile.doctor)  
    no = appointment.count() 

    context = {
        'doctors':doctor, 
        'no':no,
    }  

    return render(request,'Dashboard/doctors.html',context) 


@login_required(login_url='loginView') 
def reserveView(request):
    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete')
    
    if Profile.objects.filter(user=request.user,is_doctor=True).exists():
        return HttpResponse("Please go back,this page it's only for user's.")
    
    context = { } 

    form = AppointmentForm(request.POST or None) 
    
    try:
        if form.is_valid():
            doctor = request.user.profile.doctor
            form.instance.doctor = doctor
            form.save() 
            messages.success(request, 'Your appointment is saved.') 
            return redirect('reserveView')
    except IntegrityError: 
        messages.success(request, 'The date and time you selected are reserved!')
        return redirect('reserveView')
        
             
             
         
    context['form']= form
    
    return render(request,'Dashboard/reserve.html',context) 


@login_required(login_url='loginView') 
def calendarView(request):    
    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete')
    
    if Profile.objects.filter(user=request.user,is_doctor=True).exists():
        return HttpResponse("Please go back,this page it's only for user's.") 
    

    dates = getDateList() 
    context = {  
        'dates':dates, 
    } 
    return render(request, 'Dashboard/calendar.html',context)


@login_required(login_url='loginView') 
def calendarDateView(request,date): 
    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete') 

    if Profile.objects.filter(user=request.user,is_doctor=True).exists():
        return HttpResponse("Please go back,this page it's only for user's.") 

    appointment = Appointment.objects.filter(doctor=request.user.profile.doctor,date=date)  
    no = appointment.count() 

    context = { 
        'app':appointment, 
        'timeslot':timeslot,
        'no':no,  
        'date':date,
    }
    
    return render(request, 'Dashboard/calendarTimeslots.html',context)


#login's coming from social networks  
@login_required(login_url='loginView') 
def complete_social(request): 
    if Profile.objects.filter(user=request.user).exists():
        return redirect('complete')
    Profile.objects.create(user=request.user)
    return redirect('complete')

@login_required(login_url='loginView') 
def complete(request):

    #login's coming from facebook 
    user = request.user.profile
    form = ProfileForm(instance=user) 

    if Profile.objects.filter(user=request.user,promise=False).exists():
        if request.method == 'POST':
            form = ProfileForm(request.POST,instance=user)
            if form.is_valid():
                form.save()
                return redirect('profileView')   

    if Profile.objects.filter(user=request.user,promise=True).exists():
        return redirect('profileView') 

    context = {'form':form,}
     

    return render(request,'Dashboard/complete.html',context)


@login_required(login_url='loginView') 
def report(request,date):
    if Profile.objects.filter(user=request.user,promise=False).exists():
        return redirect('complete') 

    appointment = Appointment.objects.filter(doctor=request.user.profile.doctor,date=date)      

    #Create report  
    appointmentlist = list(appointment)
    app_list = []
    for a in appointmentlist:
        app_list.append(a.time)
    wb = Workbook()
    wb = createReport(request.user,date,app_list) 

    if wb:
        #response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response = HttpResponse(save_virtual_workbook(wb),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename='+str(request.user)+'_'+str(date)+'_report'+'.xlsx'
        return response
