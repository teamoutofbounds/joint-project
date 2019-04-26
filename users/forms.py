from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    user_type = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')
        exclude = ('user_permissions', 'last_login', 'is_superuser',
                   'is_staff', 'is_active', 'date_joined')


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)

        self.base_fields['username'].widget.attrs['class'] = 'form-control'
        self.base_fields['username'].widget.attrs['placeholder'] = 'Nom d\'usuari'

        self.base_fields['password'].widget.attrs['class'] = 'form-control'
        self.base_fields['password'].widget.attrs['placeholder'] = 'Contrasenya'
