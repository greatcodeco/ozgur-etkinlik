from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "content", 'category', "starter_date", "finish_date", 'city', 'location']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)  # kalıtım aldığı init fonksiyonları
        for field in self.fields:
            # print(field, self.fields[field])
            self.fields[field].widget.attrs = {'class': 'form-control'}
