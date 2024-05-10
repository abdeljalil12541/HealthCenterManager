from datetime import date
from django.db import models
from django.utils import timezone

# Create your models here.


class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    
    name = models.CharField(max_length=200)
    age = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=True, default='male')
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=250, null=True)
    added_time = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    def total_visit_amount(self):
        return sum(visit.amount for visit in self.visit_set.all())
    
    
    

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    detail = models.TextField(null=True)
    medecine_detail = models.TextField(null=True)
    note = models.CharField(max_length=250, null=True)
    next_visit = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    visit_date = models.DateField(default=timezone.now)