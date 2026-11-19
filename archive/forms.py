from django import forms
from .models import Work

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ["title", "content", "year", "supervisor", "grade", "is_defended", "discipline", "keywords"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
            "keywords": forms.CheckboxSelectMultiple(),
        }