from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'you@example.com',
            }
        ),
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'Create a password',
            }
        ),
    )
    password2 = forms.CharField(
        label='Confirm password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'Repeat your password',
            }
        ),
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class EmailLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'name@example.com',
            }
        ),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'Enter your password',
            }
        ),
    )