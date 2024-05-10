from django.contrib import admin
from .models import Patient, Visit

# Register your models here.


admin.site.register(Patient)
admin.site.register(Visit)