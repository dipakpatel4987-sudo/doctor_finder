from django import forms
from .models import Availability

INPUT = {'class': 'form-input'}


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['weekday', 'start_time', 'end_time']
        widgets = {
            'weekday': forms.Select(attrs=INPUT),
            'start_time': forms.TimeInput(attrs={**INPUT, 'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={**INPUT, 'type': 'time'}, format='%H:%M'),
        }
        labels = {'weekday': 'Din', 'start_time': 'Shuru', 'end_time': 'Khatam'}

    def clean(self):
        data = super().clean()
        s, e = data.get('start_time'), data.get('end_time')
        if s and e and e <= s:
            raise forms.ValidationError('Khatam hone ka time shuru ke baad ka hona chahiye.')
        return data