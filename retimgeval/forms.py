from django import forms

from .models import Answer, Consent


class ConsentForm(forms.ModelForm):
    class Meta:
        model = Consent
        fields = ["consented"]

    def __init__(self, *args, **kwargs):
        super(ConsentForm, self).__init__(*args, **kwargs)
        self.fields["consented"].required = True
        self.fields["consented"].label = "Consent"


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["choice"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["choice"].widget = forms.RadioSelect()
        self.fields["choice"].empty_label = None
        self.fields["choice"].label = ""
