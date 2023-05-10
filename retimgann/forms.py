from django import forms

from .models import Annotation, Consent, Image


class ConsentForm(forms.ModelForm):
    class Meta:
        model = Consent
        fields = ["consented"]

    def __init__(self, *args, **kwargs):
        super(ConsentForm, self).__init__(*args, **kwargs)
        self.fields["consented"].required = True


class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ["coordinates"]
