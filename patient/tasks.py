from datetime import date, timedelta
from email.message import EmailMessage
from .models import Visit
from django.template.loader import render_to_string


def send_next_visit_email_notification(request):
    patients = Visit.objects.filter(visit_date=date.today())
    
    count = 0
    
    for patient in patients:
        nextVisitDate = patient.visit_date+timedelta(days=patient.next_visit)
        notificationDate = nextVisitDate-timedelta(days=1)
        
        if notificationDate == date.today():
            subject = 'Thank You for registering to our site'
            message = render_to_string('email_template.html', {'next_visit':nextVisitDate, 'patient':patient})
            email_from = 'sellingonlinecourses@gmail.com'
            reciept_list = [patient.patient.email,]
            mail = EmailMessage(subject, message, email_from, reciept_list)
            mail.content_subtype = "html"
            mail.send()
            count += 1
            print('notification has been sent')
    print('notif counts' + count)
    