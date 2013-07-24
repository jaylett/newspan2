from django import forms
from django.contrib.auth.forms import AuthenticationForm as AuthForm
from django.utils.translation import ugettext_lazy as _


class AuthenticationForm(AuthForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=True))
