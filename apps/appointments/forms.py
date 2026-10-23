from datetime import date
from django import forms

from apps.doctors.models import Doctor
from .models import Appointment, Review

INPUT = {'class': 'form-input'}


class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs=INPUT),
            'date': forms.DateInput(attrs={**INPUT, 'type': 'date'}),
            'time': forms.TimeInput(attrs={**INPUT, 'type': 'time'}),
            'reason': forms.Textarea(attrs={**INPUT, 'rows': 3}),
        }
        labels = {'reason': 'Reason (optional)'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True)
        self.fields['doctor'].empty_label = '-- Doctor chuniye --'
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError('Purani date nahi chun sakte.')
        return d

    def clean(self):
        data = super().clean()
        doctor, d, t = data.get('doctor'), data.get('date'), data.get('time')
        if doctor and d and t:
            taken = Appointment.objects.filter(doctor=doctor, date=d, time=t).exclude(status='Cancelled')
            if taken.exists():
                raise forms.ValidationError('Is doctor ka ye time slot pehle se book hai. Dusra time chuniye.')
        return data
class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={**INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={**INPUT, 'type': 'time'}, format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError('Purani date nahi chun sakte.')
        return d

    def clean(self):
        data = super().clean()
        d, t = data.get('date'), data.get('time')
        if d and t:
            taken = (Appointment.objects
                     .filter(doctor=self.instance.doctor, date=d, time=t)
                     .exclude(pk=self.instance.pk)
                     .exclude(status='Cancelled'))
            if taken.exists():
                raise forms.ValidationError('Is doctor ka ye time slot pehle se book hai. Dusra time chuniye.')
        return data
class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        label='Rating',
        coerce=int,
        choices=[(5, '★★★★★  Bahut achha'), (4, '★★★★☆  Achha'), (3, '★★★☆☆  Theek-thaak'),
                 (2, '★★☆☆☆  Kamzor'), (1, '★☆☆☆☆  Bahut kharab')],
        widget=forms.Select(attrs=INPUT),
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {'comment': forms.Textarea(attrs={**INPUT, 'rows': 3})}
        labels = {'comment': 'Comment (optional)'}