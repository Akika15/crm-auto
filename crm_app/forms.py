from django import forms
from .models import Client, Order, ServiceReminder

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'middle_name', 'phone', 'email', 'address', 'comments']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'vehicle', 'status', 'payment_method', 'delivery_method', 'comments']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_method': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = ServiceReminder
        fields = ['client', 'vehicle', 'reminder_type', 'last_service_date', 'last_service_mileage', 
                  'interval_days', 'interval_km', 'scheduled_date', 'consent_given']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'reminder_type': forms.Select(attrs={'class': 'form-control'}),
            'last_service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_service_mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'interval_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'interval_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'consent_given': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }