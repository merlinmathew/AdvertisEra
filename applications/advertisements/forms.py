from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Advertisement
from django.contrib.auth.forms import AuthenticationForm

__author__ = 'Merlin'

from django.contrib.auth.forms import AuthenticationForm

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
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }

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
        cleaning password.
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password_mismatch')


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
        # self.fields['is_featured'].widget.attrs['onclick'] = "calc();"


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
