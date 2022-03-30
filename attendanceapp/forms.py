from django import forms

from .models import Person


class PersonForm(forms.ModelForm):

    image = forms.ImageField()
 
    class Meta:
        model = Person
        fields = ['name', 'image']
