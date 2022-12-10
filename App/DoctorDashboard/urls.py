from django.urls import path 
from . import views

urlpatterns = [
    path('doctor-dashboard',views.doctorDashboard,name='doctorDashboard'),
    path('manage',views.manageView,name='manageView'),
    path('convert',views.convertView,name='convertView'),
    path('patients',views.patientView,name='patientView'),
    path('delete/<int:id>',views.deleteView,name='deleteView'),
]
