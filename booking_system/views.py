# -*- coding: utf-8 -*-
from .models import Booking,Customer,Dog
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from .forms import User_Form
from django.forms import ModelForm
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'booking_system/index.html'
    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all().order_by('time','slot')
        elif self.request.user.is_authenticated():
            return Booking.objects.filter(customer=self.request.user).order_by('time','slot')
class DetailView(generic.DetailView):
    template_name = 'booking_system/booking.html'
    def get_object(self):
        if self.request.user.is_staff:
            return get_object_or_404(Booking,pk=self.kwargs['booking_id'])
        elif self.request.user.is_authenticated():
            return get_object_or_404(Booking,pk=self.kwargs['booking_id'],customer=self.request.user)
        else:
            pass
class Customer_Detail_View(generic.DetailView):
    template_name = 'booking_system/customer.html'
    def get_object(self):
        return get_object_or_404(Customer,user=self.request.user)
class Customer_Edit_View(UpdateView):
    fields = ['mobile_number','home_number','work_number','home_address']
    model = Customer
    def get_object(self):
        return get_object_or_404(Customer,user=self.request.user)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Customer_Edit_View, self).form_valid(form)
    success_url = reverse_lazy("booking_system:customer")
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['dog', 'time','slot', 'comment','option']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BookingForm,self).__init__(*args, **kwargs)
        self.fields['dog'].queryset = Dog.objects.filter(owner=user)
class Booking_Create_View(CreateView):
    template_name = 'booking_system/booking_form.html'
    form_class = BookingForm
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(Booking_Create_View, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(Booking_Create_View,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    success_url = reverse_lazy("booking_system:index")
class Booking_Edit_View(UpdateView):
    template_name = 'booking_system/booking_form.html'
    form_class = BookingForm
    def get_object(self):
        return get_object_or_404(Booking,pk=self.kwargs['booking_id'],customer=self.request.user)
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(Booking_Edit_View, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(Booking_Edit_View,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    success_url = reverse_lazy("booking_system:index")
class Booking_Delete_View(DeleteView):
    model = Booking
    success_url =  reverse_lazy("booking_system:index")
class Staff_Booking_Create_View(CreateView):
    fields = ['time','slot']
    template_name = 'booking_system/time_manage.html'
    model = Booking
    def form_valid(self, form):
        form.instance.customer = self.request.user
        form.instance.dog = get_object_or_404(Dog,pk=13)
        form.instance.comment = 'STAFF BUSY'
        return super(Staff_Booking_Create_View, self).form_valid(form)
    success_url = reverse_lazy("booking_system:index")
class Dog_Index_View(generic.ListView):
    template_name = 'booking_system/dog_index.html'
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Dog.objects.filter(owner=self.request.user).order_by('name')
        else:
            pass#todo: some customer logic
class Dog_Create_View(CreateView):
    template_name = 'booking_system/dog_form.html'
    fields = ['name','breed','date_of_birth']
    model = Dog
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(Dog_Create_View, self).form_valid(form)
    success_url = reverse_lazy("booking_system:dog-index")
class Dog_Edit_View(UpdateView):
    fields = ['name','breed','date_of_birth']
    model = Dog
    def get_object(self):
        return get_object_or_404(Dog,pk=self.kwargs['dog_id'],owner=self.request.user)
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(Dog_Edit_View, self).form_valid(form)
    def get_success_url(self):
        return reverse('booking_system:dog-detail', args=(self.kwargs['dog_id']))
class Dog_Delete_View(DeleteView):
    model = Dog
    success_url =  reverse_lazy("booking_system:dog-index")
class Dog_Detail_View(generic.DetailView):
    template_name = 'booking_system/dog.html'
    def get_object(self):
        if self.request.user.is_authenticated():
            return get_object_or_404(Dog,pk=self.kwargs['dog_id'],owner=self.request.user)
        else:
            pass

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #Query for a user goes here
                if not user.is_staff:
                    return render(request, 'booking_system/index.html',{'object_list':Booking.objects.filter(customer=request.user)})
                else:
                    return render(request, 'booking_system/index.html',{'object_list': Booking.objects.all()})
            else:
                return render(request, 'booking_system/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'booking_system/login.html', {'error_message': 'Invalid login'})
    return render(request, 'booking_system/login.html')
def logout_user(request):
    logout(request)
    #give sample or ads in future
    return render(request, 'booking_system/index.html', {'object_list':None})
class User_Form_View(View):
    form_class = User_Form
    template_name = 'booking_system/registrate_form.html'
    #For new user
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})
    #Regist to Database
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             username = form.cleaned_data['username']
             password = form.cleaned_data['password']
             user.set_password(password)
             user.save()
             c = Customer()
             c.user = user
             c.save()
             user = authenticate(username=username,password=password)

             if user is not None:
                 if user.is_active:
                     login(request,user)
                     return redirect( 'booking_system:index')
                     #if wanna call info about user just write user.username
        return render(request, self.template_name, {'form': form})

def get_slot(request):
    input_time = request.GET.get('time', None)
    all_slot = ["9:00AM-10:30AM","10:30AM-12:00PM", "1:00PM-2:30PM", "2:30PM-4:00PM","4:00PM-5:30PM" ]
    all_slot_id = ["S0","S1","S2","S3","S4"]
    free_slot = []
    free_slot_id=[]
    booked_slot=[]
    booked_slot_id = list( Booking.objects.filter(time=input_time).values_list('slot',flat=True))
    q = list(Booking.objects.filter(time=input_time))
    for slot in q:
         booked_slot.append(slot.get_slot_display())
    for slot in all_slot:
        if slot not in booked_slot:
            free_slot.append(slot)
    for slot_id in all_slot_id:
        if slot_id not in booked_slot_id:
            free_slot_id.append(slot_id)
    data = {
        'free_slot': free_slot,
        'free_slot_id':free_slot_id
    }
    return JsonResponse(data)