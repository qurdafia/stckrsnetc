from django.contrib.auth.models import User
from django import forms
# from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserRegistrationModel, OrderModel
from django.contrib.auth.forms import PasswordResetForm


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


#OrderModel form

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ('location', 'address', 'mobile', 'width', 'height', 'quantiy', 'file')
        labels = {
            'location': 'Enter Country',
            'address': 'Enter Shipping Address',
            'mobile': 'Enter Mobile Number',
            'width': 'Sticker Width (in)',
            'height': 'Sticker Height (in)',
            'quantiy': 'Quantity (no. of pcs)',
            'file': 'Upload Your File (pdf)',
        }



class OrderModelFormEdit(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ('location', 'address', 'mobile', 'width', 'height', 'quantiy', 'is_paid')
        labels = {
            'location': 'Enter Country',
            'address': 'Enter Shipping Address',
            'mobile': 'Enter Mobile Number',
            'width': 'Sticker Width (in)',
            'height': 'Sticker Height (in)',
            'quantiy': 'Quantity (no. of pcs)',
            'is_paid': 'Payment Status',
        }
