from django import forms
from .models import Sector, Part, LegalArticle


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['title', 'description', 'order']


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['sector', 'title', 'description', 'order']


class LegalArticleForm(forms.ModelForm):
    class Meta:
        model = LegalArticle
        fields = ['part', 'title', 'reference_number', 'content', 'keywords', 'source_link', 'order', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
            'keywords': forms.TextInput(attrs={'placeholder': 'tax, banking, arbitration...'}),
        }
