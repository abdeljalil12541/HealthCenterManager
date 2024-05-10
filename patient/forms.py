from django import forms
from .models import Patient, Visit



class QuickPatientForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea)
    medecine_detail = forms.CharField(widget= forms.Textarea)
    amount = forms.IntegerField(label='Amount')
    next_visit = forms.IntegerField(label='Next Visit')
    class Meta:
        model = Patient
        fields = ('name', 'age', 'gender', 'email')
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.Select(choices=Patient.GENDER_CHOICES, attrs={'placeholder': 'Gender'})
        self.fields['gender'].widget.attrs['class'] = 'form-select'  # Optional: Add a CSS class for styling
        
        
        
        


class PatientForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea)
    medecine_detail = forms.CharField(widget= forms.Textarea)
    note = forms.CharField(widget=forms.Textarea)
    amount = forms.IntegerField(label='Amount')
    next_visit = forms.IntegerField(label='Next Visit')
    class Meta:
        model = Patient
        fields = ('name', 'age', 'gender', 'email', 'mobile', 'address', 'detail', 'medecine_detail', 'note', 'amount', 'next_visit')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all fields and add the form-control class
        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control'
                
                
        self.fields['medecine_detail'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,  # Adjust this value as needed
            'cols': 30,  # Adjust this value as needed
        })
        
        self.fields['detail'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,  # Adjust this value as needed
            'cols': 30,  # Adjust this value as needed
        })
        
        
        # Customize the gender field separately
        self.fields['gender'].widget = forms.Select(choices=Patient.GENDER_CHOICES, attrs={'class': 'form-select'})
        
        
        
        
        
        
        
        
class VisitForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea)
    medecine_detail = forms.CharField(widget= forms.Textarea)
    note = forms.CharField(widget=forms.Textarea)
    amount = forms.IntegerField(label='Amount')
    next_visit = forms.IntegerField(label='Next Visit')
    class Meta:
        model = Visit
        fields = ('patient', 'detail', 'medecine_detail', 'note', 'amount', 'next_visit')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all fields and add the form-control class
        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control'
                
                
        self.fields['medecine_detail'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,  # Adjust this value as needed
            'cols': 30,  # Adjust this value as needed
        })
        
        self.fields['detail'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,  # Adjust this value as needed
            'cols': 30,  # Adjust this value as needed
        })
        
        
        
        self.fields['note'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,  # Adjust this value as needed
            'cols': 30,  # Adjust this value as needed
        })
        
        