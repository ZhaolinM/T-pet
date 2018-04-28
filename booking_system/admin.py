# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Customer,Dog,Booking
from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(Dog)
admin.site.register(Booking)