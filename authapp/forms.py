from django.contrib.auth.models import User
from django import forms
# from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserRegistrationModel, OrderModel
from django.contrib.auth.forms import PasswordResetForm

import phonenumbers
from phonenumbers import NumberParseException


class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


#Twilio forms

class VerificationForm(forms.Form):
    # country_code = forms.CharField(widget=forms.HiddenInput())
    phone_number = forms.CharField(widget=forms.HiddenInput())
    via = forms.ChoiceField(choices=[('sms', 'SMS')], initial='SMS')  

    def clean(self):
        data = self.cleaned_data
        phone_number = data['phone_number']

        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
        except NumberParseException as e:
            self.add_error('phone_number', e)


#OrderModel form

class OrderModelForm(forms.ModelForm):
    token = forms.CharField(label="Enter Verification Token")

    class Meta:
        model = OrderModel
        fields = ('location', 'address', 'width', 'height', 'quantiy', 'file')
        labels = {
            'location': 'Enter Country',
            'address': 'Enter Shipping Address',
            'width': 'Sticker Width (in)',
            'height': 'Sticker Height (in)',
            'quantiy': 'Quantity (no. of pcs)',
            'file': 'Upload Your File (pdf)'
        }

        def __init__(self, *args, **kwargs):
            super(form, self).__init__(*args, **kwargs)
            self.fields['token'].initial = ""



class OrderModelFormEdit(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ('is_paid',)
        labels = {
            'is_paid': 'Payment Status',
        }
