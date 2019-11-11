from django import forms
from django.forms import TextInput

from phone_book.models import Phone, Email
from .validators import validate_phone_number


class PhoneForm(forms.ModelForm):
    phone = forms.CharField(widget=TextInput(attrs={'autofocus': 'autofocus'}),
                            validators=[validate_phone_number])

    class Meta:
        model = Phone
        fields = ['phone', 'person']


class EmailForm(forms.ModelForm):
    email = forms.CharField(widget=TextInput(attrs={'autofocus': 'autofocus'}))

    class Meta:
        model = Email
        fields = ['email', 'person']
