from django import forms
from dal import autocomplete
from .models import TVChannel, TVProgram
from django.forms import DateField, DateInput
from django.forms import widgets

class DateInput(DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date = DateField(widget=DateInput)

class TVProgramForm(forms.ModelForm):
    class Meta:
        model = TVProgram
        # fields = ["title", "tv_channel", "date", "cover"]
        fields = "__all__"
        widgets = {
            "tv_channel": autocomplete.ModelSelect2(
                url="tv:tv_channel_autocomplete"),
            "date": forms.DateInput(attrs={'type': 'datetime-local'})
        }

class TVChannelForm(forms.ModelForm):
    class Meta:
        model = TVChannel
        fields = "__all__"