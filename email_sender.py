import sys,os,django,datetime,smtplib
sys.path.append('dir to project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'writter.settings'
django.setup()
#setup django ORM outside of django
from booking_system.models import Booking
arg = sys.argv[1]
EMAIL_ACCOUNT = ''
EMAIL_PWD = ''
now = datetime.datetime.now()
check_date = now+datetime.timedelta(days=1)
def send_email(receiver_addresss):
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(EMAIL_ACCOUNT,EMAIL_PWD)
    message = "You have a booking with us in 24 hours."
    s.sendmail(EMAIL_ACCOUNT,receiver_addresss,message)
    s.quit()
    print('email send to: '+receiver_addresss)
def query(time_slot):
    return Booking.objects.get(time=str(check_date)[0:10],notified=False,slot=time_slot)

'''
obj = Booking.objects.get(id=query(arg).id)
obj.notified = True
obj.save()
'''
send_email(query(arg).customer.username)

