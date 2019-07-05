from django import forms
from .models import Event, NewComment


class EventForm(forms.ModelForm):
    starter_date = forms.DateField(input_formats=("%d.%m.%Y",), widget=forms.DateInput(format="%d.%m.%Y"),
                                   required=True,
                                   label="Başlangıç Günü")

    class Meta:
        model = Event
        fields = ["user", "title", "content", "image", 'category', "starter_date", 'starter_time']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)  # kalıtım aldığı init fonksiyonları
        for field in self.fields:
            # print(field, self.fields[field])
            self.fields[field].widget.attrs = {'class': 'form-control'}
        DATEPICKER = {
            'type': 'text',
            'class': 'form-control',
            'autocomplete': 'off'
        }

        self.fields['starter_date'].widget.attrs.update(DATEPICKER)


class CommentForm(forms.ModelForm):
    class Meta:
        model = NewComment
        fields = ['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class SearchForm(forms.Form):
    TIME = [('any_date', 'Herhangi bir tarih'), ('today', 'Bugün'), ('tomorrow', 'Yarın'), ('tomorrow', 'Yarın'),
            ('this_weekend', 'Bu haftasonu'), ('this_week', 'Bu hafta'), ('next_week', 'Gelecek hafta'),
            ('this_mounth', 'Bu ay'), ('next_mounth', 'Gelecek ay')]

    search = forms.CharField(required=False, max_length=500,
                             widget=forms.TextInput(attrs={'placeholder': 'Event',
                                                           'class': 'form-control'}))
    location = forms.CharField(required=False, max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': 'Location',
                                                             'class': 'form-control'}))
    time = forms.ChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control'}),
                             choices=TIME, required=False)
