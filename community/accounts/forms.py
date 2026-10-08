from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import BaseUser

INPUT_CLASSES = (
    "w-full px-4 py-2 rounded-lg border border-gray-300 "
    "focus:outline-none focus:ring-2 focus:ring-[#0802C] "
    "focus:border-[#0802C]"
)

class RegisterForm(UserCreationForm):
    class Meta:
        model = BaseUser
        fields = (
            'phone',
            'full_name',
            'address',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES


class LoginForm(AuthenticationForm):
    class Meta:
        model = BaseUser
        fields = (
            'phone',
            'password'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES
