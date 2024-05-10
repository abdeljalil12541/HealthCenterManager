from datetime import date, timedelta
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import calendar
from django.db import IntegrityError, transaction


from django.urls import reverse_lazy

from .models import Patient, Visit
from .forms import QuickPatientForm, PatientForm, VisitForm
from django.db.models import Count, Sum

# Create your views here.


def home(request):
    return render(request, 'home.html')




# Doctor Login
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            redirect('doctor_login')
    return render(request, 'login.html',{'page_title':'Doctor Login'})



# Log Out
def doctor_logout(request):
    logout(request)
    return redirect('/')
    




# Reset Password
def doctor_reset_password(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'password reset successfull')
        return redirect('doctor_login')

    return render(request, 'reset-password.html')




def doctor_dashboard(request):
    totalPatients = Patient.objects.count()
    totalCollection = Visit.objects.aggregate(total=Sum('amount'))
    return render(request, 'doctor-dashboard.html', {
        'page_title': 'Dashboard',
        'totalPatients':totalPatients,
        'totalCollection':totalCollection,
    })




# Doctor Quick Add Patient
def quick_add_patient(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = QuickPatientForm(request.POST)
                if form.is_valid():
                    patient = form.save()
                    visit = Visit.objects.create(
                        patient = patient,
                        detail = form.cleaned_data['detail'],
                        medecine_detail = form.cleaned_data['medecine_detail'],
                        next_visit = form.cleaned_data['next_visit'],
                        amount = form.cleaned_data['amount']
                    )
                    print(f'====visit==== {visit}')
                    messages.success(request, 'Patient added successfully.')
                    
                    
                    # Send Notification
                    patientsNotif = Visit.objects.filter(patient=patient, visit_date=date.today())
                    
                    count = 0
                    
                    for patient in patientsNotif:
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
                            
                    return redirect('quick_add_patient')
                else:
                    messages.warning(request, 'Sorry.. Something went wrong!!')
                    return redirect('quick_add_patient')
        except IntegrityError:
            messages.warning(request, 'Sorry.. Something went wrong!!')
            return redirect('quick_add_patient')
    else:
        form = QuickPatientForm()
        
    return render(request, 'quick-add-patient-form.html', {'form':form})






def all_patients(request):
    patients = Patient.objects.all().order_by('-id')
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = PatientForm(request.POST)
                if form.is_valid():
                    patient = form.save()
                    visit = Visit.objects.create(
                        patient = patient,
                        detail = form.cleaned_data['detail'],
                        medecine_detail = form.cleaned_data['medecine_detail'],
                        next_visit = form.cleaned_data['next_visit'],
                        amount = form.cleaned_data['amount'],
                        note = form.cleaned_data['note']
                    )
                    # Send Notification for the patient just added
                    patientsNotif = Visit.objects.filter(patient=patient, visit_date=date.today())

                    count = 0

                    for patientNotif in patientsNotif:
                        nextVisitDate = patientNotif.visit_date + timedelta(days=patientNotif.next_visit)
                        notificationDate = nextVisitDate - timedelta(days=1)

                        if notificationDate == date.today():
                            subject = 'Thank You for registering to our site'
                            message = render_to_string('email_template.html', {'next_visit': nextVisitDate, 'patient': patientNotif})
                            email_from = 'sellingonlinecourses@gmail.com'
                            receipt_list = [patientNotif.patient.email,]
                            mail = EmailMessage(subject, message, email_from, receipt_list)
                            mail.content_subtype = "html"
                            mail.send()
                            count += 1
                            print('notification has been sent')

                    messages.success(request, 'Submission completed successfully.')
                    return redirect('all_patients')
                else:
                    messages.warning(request, 'Sorry.. Something went wrong!!')
        except IntegrityError:
            messages.warning(request, 'Sorry.. Something went wrong!!')
            return redirect('quick_add_patient')
    else:
        form = PatientForm()
            
    return render(request, 'all-patients.html', {'patients':patients, 'form':form})




# Add Visit for Patient
def add_visit(request, patient_id):
    if request.method == 'POST':
        patient = Patient.objects.get(id= patient_id)
        form = VisitForm(request.POST)
        if form.is_valid():
            form.patient = patient
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            messages.success(request, 'Visit added successfully')
            return redirect(reverse_lazy('add_visit', kwargs={'patient_id':patient_id}))    
        else:
            print(form.errors)
            messages.warning(request, 'Something went wrong')
            return redirect(reverse_lazy('add_visit', kwargs={'patient_id':patient_id}))    
    else:
        form=VisitForm
        return render(request, 'visit-form.html', {
            'form':form,
            'page_title': 'Add Visit'
        })



# Add Patient
def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)  # Pass the instance here
        if form.is_valid():
            form.save()
            # Send Notification
            patientsNotif = Visit.objects.filter(patient=patient, visit_date=date.today())
            
            count = 0
            
            for patient in patientsNotif:
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
            messages.success(request, 'Patient updated successfully.')
            return redirect('all_patients')
        else:
            messages.warning(request, 'Sorry.. Something went wrong!!')
    else:
        form = PatientForm(instance=patient)
        
    return render(request, 'update-patients.html', {'form': form, 'patient':patient})


def delete_patient(request, id):
    Patient.objects.get(id=id).delete()
    messages.success(request, 'Patient deleted successfully.')
    return redirect('all_patients')




def email_template(request):
    return render(request, 'email_template.html')

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone

def n_patients(request):
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

    return render(request, 'n_patients.html', {'patients': patients, 'count':count})



def reports(request):
    selectedYear = date.today().year
    if request.GET.get('year'):
        selectedYear = request.GET.get('year')
        
        
    selectedMonth = date.today().month
    if request.GET.get('month'):
        selectedMonth = request.GET.get('month')
    
    
    # Fetch Years
    years = Visit.objects.values('visit_date__year').annotate(total=Count('id'))
    
    
    # Fetch Months
    monthNames = [] 
    months = Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
    for month in months:
        monthNames.append({'id':month['visit_date__month'], 'name':calendar.month_name[month['visit_date__month']]})
    
    
    # Chart By Dates
    dPatients = Visit.objects.filter(visit_date__year=selectedYear, visit_date__month=selectedMonth).values('visit_date').annotate(total=Count('id'))
    dailyChartLabels = []
    dailyChartValues = []
    
    for data in dPatients:
        dailyChartLabels.append(data['visit_date'].strftime('%d-%m-%y'))
        dailyChartValues.append(data['total'])
        
        
    
    # Chart By Months
    mPatients = Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
    monthChartLabels = []
    monthChartValues = []
    
    for data in mPatients:
        monthName = calendar.month_name[data['visit_date__month']]
        monthChartLabels.append(monthName)
        monthChartValues.append(data['total'])
        
        
    
    # Chart By Years
    yPatients = Visit.objects.values('visit_date__year').annotate(total=Count('id'))
    yearChartLabels = []
    yearChartValues = []
    
    for data in yPatients:
        yearName = data['visit_date__year']
        yearChartLabels.append(yearName)
        yearChartValues.append(data['total'])
        
    
    return render(request, 'reports.html', {
        
        'dailyPatients': dPatients, 
        
        'page_title':'Reports',
        
        'dailyChart':{
            'dailyChartLabels':dailyChartLabels, 'dailyChartValues':dailyChartValues
            },
        'monthlyChart':{
            'monthlyChartLabels':monthChartLabels, 'monthlyChartValues':monthChartValues
            },
        'yearlyChart':{
            'yearlyChartLabels':yearChartLabels, 'yearlyChartValues':yearChartValues
            },
        
        'years':years,
        
        'currentYear': int(selectedYear),
        'currentMonth': int(selectedMonth),
        
        'monthNames':monthNames,
        
        })
    
    
    
    
    
def colection_reports(request):
    selectedYear = date.today().year
    if request.GET.get('year'):
        selectedYear = request.GET.get('year')
        
        
    selectedMonth = date.today().month
    if request.GET.get('month'):
        selectedMonth = request.GET.get('month')
    
    
    # Fetch Years
    years = Visit.objects.values('visit_date__year').annotate(total=Count('id'))
    
    
    # Fetch Months
    monthNames = [] 
    months = Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
    for month in months:
        monthNames.append({'id':month['visit_date__month'], 'name':calendar.month_name[month['visit_date__month']]})
    
    
    # Chart By Dates
    dPatients = Visit.objects.filter(visit_date__year=selectedYear, visit_date__month=selectedMonth).values('visit_date').annotate(total=Sum('amount'))
    dailyChartLabels = []
    dailyChartValues = []
    
    for data in dPatients:
        dailyChartLabels.append(data['visit_date'].strftime('%d-%m-%y'))
        dailyChartValues.append(float(data['total']))
        
        
    
    # Chart By Months
    mPatients = Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Sum('amount'))
    monthChartLabels = []
    monthChartValues = []
    
    for data in mPatients:
        monthName = calendar.month_name[data['visit_date__month']]
        monthChartLabels.append(monthName)
        monthChartValues.append(float(data['total']))
        
        
    
    # Chart By Years
    yPatients = Visit.objects.values('visit_date__year').annotate(total=Sum('id'))
    yearChartLabels = []
    yearChartValues = []
    
    for data in yPatients:
        yearName = data['visit_date__year']
        yearChartLabels.append(yearName)
        yearChartValues.append(float(data['total']))
        
    return render(request, 'colection-reports.html', {
        
        'dailyPatients': dPatients, 
        
        'page_title':'Reports',
        
        'dailyChart':{
            'dailyChartLabels':dailyChartLabels, 'dailyChartValues':dailyChartValues
            },
        'monthlyChart':{
            'monthlyChartLabels':monthChartLabels, 'monthlyChartValues':monthChartValues
            },
        'yearlyChart':{
            'yearlyChartLabels':yearChartLabels, 'yearlyChartValues':yearChartValues
            },
        
        'years':years,
        
        'currentYear': int(selectedYear),
        'currentMonth': int(selectedMonth),
        
        'monthNames':monthNames,
        
        })