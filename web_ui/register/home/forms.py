from django.contrib.auth import get_user_model
from django import forms

from home.models import Urls

User = get_user_model()


class DataForm(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ('urls',)
        labels = {
            'urls': 'Ссылка'
        }
