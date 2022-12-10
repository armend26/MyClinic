from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
 
class Appointment(models.Model):
    """Contains info about appointment"""

    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')
    
    TIMESLOT_LIST = (
        (0, '08:00 – 08:30'),
        (1, '08:30 – 09:00'),
        (2, '09:00 – 09:30'),
        (3, '09:30 – 10:00'),
        (4, '10:00 - 10:30'), 
        (5, '10:30 - 11:00'),
        (6, '11:00 - 11:30'), 
        (7, '11:30 - 12:00'), 
        (8, '12:00 – 12:30'),
        (9, '12:30 – 13:00'),
        (10, '13:00 – 13:30'),
        (11, '13:30 – 14:00'),
        (12, '14:00 – 14:30'),
        (13, '14:30 – 15:00'),
        (14, '15:00 – 15:30'),
        (15, '15:30 – 16:00'),
    )
 
    doctor = models.ForeignKey('Doctor',on_delete = models.CASCADE,null=True) 
    date = models.DateField()
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    note = models.CharField(default="",max_length=300)

    def __str__(self):
        return '{} {} {}. Info: {}'.format(self.date, self.time, self.doctor, self.note )

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Doctor(models.Model):
    """Stores info about doctor"""
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    education = models.CharField(max_length=30)  
    quote = models.CharField(max_length=300)

    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)

class Profile(models.Model):
    user = models.OneToOneField(User,blank=True,on_delete=models.CASCADE) 
    doctor = models.ForeignKey('Doctor',on_delete = models.CASCADE,null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    promise = models.BooleanField(default=False)
    
    def __str__(self):
        return '{} {}'.format(self.user, self.birth_date)

 