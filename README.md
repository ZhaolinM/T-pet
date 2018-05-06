
To run:
    go to the location of manage.py 
    
    
    python manage.py runserver
You may need to fix the dir and email account&password in email_sender.py

to run email_sender(in linux shell):
     
     watch -n X python email_sender.py
X is the time interval you want to run the script(in second), also gmail cannot send more than 500 mails per day in this way
