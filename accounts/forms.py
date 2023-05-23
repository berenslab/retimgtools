from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Permission
from environs import Env
from unique_names_generator import get_random_name

from .models import InvitationCode

env = Env()
env.read_env()

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    experience = forms.IntegerField(required=True)
    experience.help_text = "Enter your year of experience"

    invitation_code = forms.CharField(required=True)
    invitation_code.help_text = "Enter the invitation code you received"

    class Meta:
        model = User
        fields = ("username", "experience", "invitation_code")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].initial = "_".join(get_random_name().lower().split(" "))
        self.fields[
            "username"
        ].help_text = "Modify your username if you want. For anonymity purpose, we don't record your email address, so you can't reset your password if you forget your username and password. Please write down your username and password somewhere safe."

    def clean_invitation_code(self):
        code = self.cleaned_data.get("invitation_code")
        # Check if the code is the passcode
        if code == env.str("PASSCODE"):  # replace with your actual passcode
            return code
        # If not, check if it's a valid invitation code
        try:
            invitation = InvitationCode.objects.get(code=code)
            if invitation.is_used:
                raise forms.ValidationError(
                    "This invitation code has already been used"
                )
        except InvitationCode.DoesNotExist:
            raise forms.ValidationError("The code you entered is incorrect")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        code = self.cleaned_data.get("invitation_code")
        # Only mark the invitation code as used if it's not the passcode
        if code != env.str("PASSCODE"):  # replace with your actual passcode
            invitation = InvitationCode.objects.get(code=code)
            invitation.is_used = True
            invitation.save()
            user.code_used = invitation.code
        else:
            user.is_staff = True
            user.code_used = "passcode"

        if commit:
            user.save()

            # Give the user permissions to view and edit multiple models
            if user.is_staff:
                app_model_pairs = [
                    ("accounts", "invitationcode"),
                    ("retimgann", "annotation"),
                    ("retimgeval", "answer"),
                ]

                for app_label, model_name in app_model_pairs:
                    permissions = Permission.objects.filter(
                        content_type__app_label=app_label,
                        content_type__model=model_name,
                    )
                    for permission in permissions:
                        user.user_permissions.add(permission)

        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "experience")
