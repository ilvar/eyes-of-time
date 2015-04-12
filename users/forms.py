from django import forms

from users.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']