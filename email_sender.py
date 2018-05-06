import sys,os,django,datetime,smtplib
sys.path.append('dir to project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'writter.settings'
django.setup()
#setup django ORM outside of django



from booking_system.models import Booking

now = datetime.datetime.now()
check_date = now+datetime.timedelta(days=1)
print('Today is:'+str(now)[0:10])
print('Check for booking at:'+str(check_date)[0:10])

raw_result = list(Booking.objects.filter(time=str(check_date)[0:10],notified=False))
email_address = list(map(lambda x:x.customer.username,raw_result))
def send_email(receiver_addresss):
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login('gmail_account','gmail_password')
    message = "You have a booking with us"
    s.sendmail('gmail_account',receiver_addresss,message)
    s.quit()
    print('email send to: '+receiver_addresss)
send_email(email_address[0])
