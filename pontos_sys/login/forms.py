from django import forms
from .models import CustomUser, Transaction, Requests
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.Select(choices=model.AMOUNT_CHOICES)
        }
    
    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)  # Pop the 'users' argument
        super().__init__(*args, **kwargs)
        
        if users:
            """ self.fields['reciever'].widget = forms.TextInput() """
            """ self.fields['reciever'].queryset = users
            self.fields['reciever'].widget.attrs.update({'class': 'custom-field'}) """
            self.fields['amount'].widget.attrs.update({'class': 'custom-field'})
            self.fields['description'].widget.attrs.update({'class': 'custom-field'})
        
        
class UserTextInput(forms.TextInput):
    def format_value(self, value):
        try:
            user = CustomUser.objects.get(email=value)
            return user.email
        except ObjectDoesNotExist:
            return value
        
class RequestForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['requester']