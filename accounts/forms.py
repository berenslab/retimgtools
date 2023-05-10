from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from unique_names_generator import get_random_name

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    experience = forms.IntegerField(required=True)
    experience.help_text = "Enter your year of experience"

    class Meta:
        model = User
        fields = ("username", "experience")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].initial = "_".join(get_random_name().lower().split(" "))
        self.fields[
            "username"
        ].help_text = "Modify your username if you want. For anonymity purpose, we don't record your email address, so you can't reset your password if you forget your username and password. Please write down your username and password somewhere safe."

    def save(self, commit=True):
        experience = self.cleaned_data.get("experience", None)
        return super().save(commit=commit)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "experience")
