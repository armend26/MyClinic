from django.urls import path 
from . import views 

urlpatterns = [
    path('dashboard/',views.dashboardView,name='dashboardView'), 
    path('profile/',views.profileView,name='profileView'), 
    path('doctors/',views.doctorView,name='doctorView'), 
    path('reserve/',views.reserveView,name='reserveView'), 
    path('calendar/',views.calendarView,name='calendarView'),
    path('calendar/<date>',views.calendarDateView,name='calendarDateView'),
    path('report/<date>',views.report,name='report'),
    path('complete/',views.complete,name='complete'), 
    path('complete-social/',views.complete_social,name='complete_social'),
   
]
 