from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import TextInput
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
        }


class DataForm(forms.Form):
    data = forms.CharField()
