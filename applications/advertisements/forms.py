from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from .models import Advertisement
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField

__author__ = 'Merlin'


class RegistrationForm(forms.ModelForm):
    """
    form for registration.
    """
    confirm_password = forms.CharField(label=_("Confirm Password"), required=True,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password*', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].required = True
        self.fields['username'].widget.attrs['placeholder'] = 'Username*'
        self.fields['email'].widget.attrs['placeholder'] = 'Email*'
        self.fields['password'].widget.attrs['placeholder'] = 'Password*'

    def clean(self):
        """
        to clean password.
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password_mismatch')

    def clean_username(self):
        """
        to clean username.
        """
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError('This username has been taken.Please Try Another One :)')
        return username

    def clean_email(self):
        """
        to clean email.
        """
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('This email has been taken.Please Try Another One :)')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password


class LoginForm(AuthenticationForm):
    """
    form for login
    """

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username*'
        self.fields['password'].widget.attrs['placeholder'] = 'Password*'


class AdvertisementAddForm(forms.ModelForm):
    """
    form to add an advertisement.
    """
    class Meta:
        model = Advertisement
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(AdvertisementAddForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['type'] = "file"
        self.fields['image'].widget.attrs['accept'] = ".jpg, .jpeg, .png"
        self.fields['image'].required = True


class AdvertisementEditForm(forms.ModelForm):
    """
    form to edit advertisement.
    """
    class Meta:
        model = Advertisement
        exclude = ('is_featured',)

    def __init__(self, *args, **kwargs):
        super(AdvertisementEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['type'] = "file"
        self.fields['image'].widget.attrs['accept'] = ".jpg, .jpeg, .png"
        self.fields['image'].required = True
