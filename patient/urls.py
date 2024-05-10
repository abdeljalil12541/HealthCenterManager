from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.doctor_login, name='doctor_login'),
    path('doctor/login', views.doctor_login, name='doctor_login'),
    path('doctor/logout', views.doctor_logout, name='doctor_logout'),
    path('doctor/reset-password', views.doctor_reset_password, name='doctor_reset_password'),
    path('doctor/dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/quick-add-patient', views.quick_add_patient, name='quick_add_patient'),
    path('patients', views.all_patients, name='all_patients'),
    path('patients/update/<int:id>', views.update_patient, name='update_patient'),
    path('patients/delete/<int:id>', views.delete_patient, name='delete_patient'),
    path('patients/email_template', views.email_template, name='email_template'),
    path('patients/n_patients', views.n_patients, name='n_patients'),
    
    # Reports
    path('reports', views.reports, name='reports'),
    path('colection-reports', views.colection_reports, name='colection_reports'),

    # Add Visit
    path('patients/add-visit/<int:patient_id>', views.add_visit, name='add_visit'),
]



































# from . import views
# from django.urls import include, path

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('doctor/login', views.doctor_login, name='doctor_login'),
#     path('doctor/logout', views.doctor_logout, name='doctor_logout'),
#     path('doctor/reset-password', views.doctor_reset_password, name='doctor_reset_password'),
#     path('doctor/dashboard', views.doctor_dashboard, name='doctor_dashboard'),
#     path('doctor/quick-add-patient', views.quick_add_patient, name='quick_add_patient'),
#     path('doctor/all-patients', views.all_patients, name='all_patients'),
#     path('doctor/patients/update/<int:id>', views.update_patient, name='update_patient'),
#     path('doctor/patients/delete/<int:id>', views.delete_patient, name='delete_patient'),
#     path('doctor/patients/delete/<int:id>', views.delete_patient, name='delete_patient'),
# ]
