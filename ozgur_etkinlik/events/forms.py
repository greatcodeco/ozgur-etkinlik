from django import forms
from .models import Event, NewComment


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "content", "image", 'category', "starter_date", 'city', 'location']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)  # kalıtım aldığı init fonksiyonları
        for field in self.fields:
            # print(field, self.fields[field])
            self.fields[field].widget.attrs = {'class': 'form-control'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = NewComment
        fields = ['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
