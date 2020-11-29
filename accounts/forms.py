from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import UserProfile
from core.mixins import BootStrapFormMixin


class SignUpForm(UserCreationForm, BootStrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_form()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'profile_picture',
        )
