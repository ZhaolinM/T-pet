# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_address = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=20)
    home_number = models.CharField(max_length=20,blank=True)
    work_number = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.user.first_name+' , Phone num is '+self.mobile_number

class Dog(models.Model): #dog is 1-N for customer
    owner = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    date_of_birth = models.CharField(max_length=20)#TODO

    def __str__(self):
        return self.name+' belongs to '+self.owner.first_name

class Booking(models.Model):# Booking is 1-N for dog
    customer = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog,on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    time = models.DateField()
    slot_choice = (
        ('S0','9:00AM-10:30AM'),
        ('S1','10:30AM-12:00PM'),
        ('S2','1:00PM-2:30PM'),
        ('S3', '2:30PM-4:00PM'),
        ('S4', '4:00PM-5:30PM'),
    )
    slot = models.CharField(max_length=20,choices=slot_choice, default='S0')
    option_choice = (
        ('WO', 'Wash Only'),
        ('WN', 'Wash&nail clip'),
        ('DG', 'Deluxe Grooming'),
    )
    option = models.CharField(max_length=20,choices=option_choice, default='WO')
    notified = models.BooleanField(default=False)

    def __str__(self):
        return 'For '+self.dog.name+' , date is '+ self.time.strftime('%Y-%m-%d') + ', time is '+self.get_slot_display()