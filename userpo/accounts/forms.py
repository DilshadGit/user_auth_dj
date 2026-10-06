from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='First name',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'First name',
            }
        ),
    )
    last_name = forms.CharField(
        label='Last name',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'Last name',
            }
        ),
    )
    mobile_number = forms.CharField(
        label='Mobile number',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': '+0000000000',
            }
        ),
    )
    address = forms.CharField(
        label='Address',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'Street address',
            }
        ),
    )
    postcode = forms.CharField(
        label='Postcode',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'placeholder': 'Postcode',
            }
        ),
    )
    date_of_birth = forms.DateField(
        label='Date of birth',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control form-control-lg text-center',
                'type': 'date',
            }
        ),
    )
    barcode_number = forms.CharField(
        label='Barcode number',
        required=False,
        widget=forms.HiddenInput(),
    )
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
        fields = ('first_name', 'last_name', 'mobile_number', 'address', 'postcode', 'date_of_birth', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.mobile_number = self.cleaned_data.get('mobile_number', '')
        user.address = self.cleaned_data.get('address', '')
        user.postcode = self.cleaned_data.get('postcode', '')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*',
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile_number',
            'address',
            'postcode',
            'date_of_birth',
            'bio',
            'profile_image',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg text-center', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg text-center', 'placeholder': 'Last name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control form-control-lg text-center', 'placeholder': '+0000000000'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-lg text-center', 'placeholder': 'Street address'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control form-control-lg text-center', 'placeholder': 'Postcode'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control form-control-lg text-center', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control form-control-lg text-center', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
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

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request,
                email=username,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            if not self.user_cache.is_active or self.user_cache.is_deleted:
                raise forms.ValidationError(
                    'This account is inactive or deleted.',
                    code='inactive',
                )
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
