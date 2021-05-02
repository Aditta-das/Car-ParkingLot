from django import forms
from .models import *

class CarParkForm(forms.ModelForm):
    class Meta:
        model = carPark
        fields = ('car_no',)