from django import forms
from .models import LinkItem, Profile
import re

class LinkItemForm(forms.ModelForm):
    class Meta:
        model = LinkItem
        fields = ("url", "tipo")
        widgets = {
            "url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("url") or not cleaned.get("tipo"):
            raise forms.ValidationError("Compila tutti i campi.")
        return cleaned


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar",)
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"})
        }

class BgColorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bg_color",)
        widgets = {
            "bg_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color"}),
        }