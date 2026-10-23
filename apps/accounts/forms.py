import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import User

INPUT = {'class': 'form-input'}


class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=INPUT))
    confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs=INPUT))
    role = forms.ChoiceField(
        label='Sign Up As',
        choices=[('', '-- Select --'), ('patient', 'Patient'), ('doctor', 'Doctor')],
        widget=forms.Select(attrs=INPUT),
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'phone']
        labels = {'first_name': 'Full Name', 'phone': 'Phone (10 digit)'}
        widgets = {
            'first_name': forms.TextInput(attrs=INPUT),
            'email': forms.EmailInput(attrs=INPUT),
            'phone': forms.TextInput(attrs={**INPUT, 'maxlength': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['phone'].required = True

    def clean_first_name(self):
        name = self.cleaned_data['first_name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Naam kam se kam 3 akshar ka ho.')
        return name

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ye email pehle se registered hai.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not re.fullmatch(r'[6-9]\d{9}', phone):
            raise forms.ValidationError('10 digit number daalein (6-9 se shuru).')
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        data = super().clean()
        if data.get('password') and data.get('confirm') and data['password'] != data['confirm']:
            self.add_error('confirm', 'Password match nahi karta.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.is_approved = (user.role == 'patient')  # doctor admin approval ke baad
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={**INPUT, 'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=INPUT))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'phone']
        labels = {'first_name': 'Full Name', 'phone': 'Phone (10 digit)'}
        widgets = {
            'first_name': forms.TextInput(attrs=INPUT),
            'phone': forms.TextInput(attrs={**INPUT, 'maxlength': 10}),
        }

    def clean_first_name(self):
        name = self.cleaned_data['first_name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Naam kam se kam 3 akshar ka ho.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not re.fullmatch(r'[6-9]\d{9}', phone):
            raise forms.ValidationError('10 digit number daalein (6-9 se shuru).')
        return phone