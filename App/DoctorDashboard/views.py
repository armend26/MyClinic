from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from Doctors.models import Profile,Appointment
from datetime import date
from Dashboard.datelist import getDateList
from django.contrib.auth.decorators import login_required 
from .excelDoctor import createReport
from .excelPatient import patientReport
from openpyxl import Workbook  
from openpyxl.writer.excel import save_virtual_workbook
import datetime
# Create your views here.

@login_required(login_url='loginView')
def doctorDashboard(request): 

    if Profile.objects.filter(user=request.user,is_doctor=False).exists():
        return HttpResponse("Please go back,this page it's only for staff.")  
    
    #number of total appointments
    appointment = Appointment.objects.filter(doctor=request.user.profile.doctor)  
    no = appointment.count() 

    #number of appointments today
    appointment_today = Appointment.objects.filter(doctor=request.user.profile.doctor,date=date.today().isoformat())  
    no_today = appointment_today.count()  


    context = { 
        'no':no,  
        'no_today':no_today, 
    }

    return render(request,'Dashboard/doctorDashboard.html',context)

@login_required(login_url='loginView')
def manageView(request):
    if Profile.objects.filter(user=request.user,is_doctor=False).exists():
        return HttpResponse("Please go back,this page it's only for staff.") 
    
    app = Appointment.objects.filter(doctor=request.user.profile.doctor).order_by('date','timeslot')

    context = { 'app':app, }
    
    return render(request, 'Dashboard/manageView.html',context) 

@login_required(login_url='loginView')
def convertView(request):
    if Profile.objects.filter(user=request.user,is_doctor=False).exists():
        return HttpResponse("Please go back,this page it's only for staff.") 
   
    current_time = datetime.datetime.now() 

    appointment = Appointment.objects.filter(doctor=request.user.profile.doctor).order_by('date','timeslot')      

    #Create report  
    appointmentlist = list(appointment)


    wb = Workbook()
    wb = createReport(appointmentlist) 

    if wb:
        #response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response = HttpResponse(save_virtual_workbook(wb),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename='+str(request.user)+str(current_time.microsecond)+'_report'+'.xlsx'
        return response

@login_required(login_url='loginView')
def patientView(request):
    if Profile.objects.filter(user=request.user,is_doctor=False).exists():
        return HttpResponse("Please go back,this page it's only for staff.") 

    
    current_time = datetime.datetime.now() 
    patient = Profile.objects.filter(doctor=request.user.profile.doctor).order_by('user')      

    #Create report  
    patientlist = list(patient)


    wb = Workbook()
    wb = patientReport(patientlist) 

    if wb:
        #response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response = HttpResponse(save_virtual_workbook(wb),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename='+str(request.user)+str(current_time.microsecond)+'_patients'+'.xlsx'
        return response



@login_required(login_url='loginView')
def deleteView(request,id):
    app = Appointment.objects.get(id=id)
    app.delete()
    return redirect('manageView')
 