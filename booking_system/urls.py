from django.conf.urls import url
from . import views
app_name = 'booking_system'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^login/$', views.login_user ,name = 'login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.User_Form_View.as_view(),name='register'),
    url(r'^customer/$', views.Customer_Detail_View.as_view(), name='customer'),
    url(r'^customer/edit/$', views.Customer_Edit_View.as_view(), name='customer-edit'),
    url(r'^(?P<booking_id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^booking/add/$', views.Booking_Create_View.as_view(), name='booking-add'),
    url(r'^booking/(?P<booking_id>[0-9]+)/edit/$', views.Booking_Edit_View.as_view(), name='booking-edit'),
    url(r'^booking/(?P<pk>[0-9]+)/delete/$', views.Booking_Delete_View.as_view(), name='booking-delete'),
    url(r'^dog/$', views.Dog_Index_View.as_view(),name='dog-index'),
    url(r'^dog/(?P<dog_id>[0-9]+)/$', views.Dog_Detail_View.as_view(), name='dog-detail'),
    url(r'^dog/add/$', views.Dog_Create_View.as_view(), name='dog-add'),
    url(r'^dog/(?P<dog_id>[0-9]+)/edit/$', views.Dog_Edit_View.as_view(), name='dog-edit'),
    url(r'^dog/(?P<pk>[0-9]+)/delete/$', views.Dog_Delete_View.as_view(), name='dog-delete'),
    url(r'^ajax/get_slot/$', views.get_slot, name='get_slot'),
]