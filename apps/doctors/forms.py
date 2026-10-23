from django import forms
from .models import Doctor

INPUT = {'class': 'form-input'}


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty', 'city', 'phone', 'fee', 'experience',
                  'education', 'about', 'photo', 'is_available']
        widgets = {
            'specialty': forms.Select(attrs=INPUT),
            'city': forms.TextInput(attrs=INPUT),
            'phone': forms.TextInput(attrs=INPUT),
            'fee': forms.NumberInput(attrs={**INPUT, 'min': 0}),
            'experience': forms.NumberInput(attrs={**INPUT, 'min': 0}),
            'education': forms.TextInput(attrs=INPUT),
            'about': forms.Textarea(attrs={**INPUT, 'rows': 4}),
            'photo': forms.ClearableFileInput(attrs=INPUT),
        }
        labels = {
            'fee': 'Consultation Fee (₹)',
            'experience': 'Experience (years)',
            'is_available': 'Patients ko dikhein (available)',
        }

    def clean_fee(self):
        fee = self.cleaned_data['fee']
        if fee > 20000:
            raise forms.ValidationError('Fee bahut zyada hai.')
        return fee

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'size') and photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Photo 2 MB se choti honi chahiye.')
        return photo