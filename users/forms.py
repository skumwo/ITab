from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Choose Role")

    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        try:
            validate_password(password, self.instance)
        except ValidationError:
            pass  # Отключает проверки Django
        return password