# forms.py
from django.contrib.auth.forms import SetPasswordForm
from django import forms


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email")


# forms.py


class PasswordResetConfirmForm(SetPasswordForm):
    pass
