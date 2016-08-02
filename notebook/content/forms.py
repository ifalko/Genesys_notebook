from django import forms

from .models import RecordNotebook


class RecordForm(forms.ModelForm):

    class Meta:
        model = RecordNotebook
        fields = [
            "full_name",
            "phone_number",
            "birthday",
        ]
