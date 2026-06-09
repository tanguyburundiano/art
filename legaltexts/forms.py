from django import forms
from .models import Part, Section, LegalArticle

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['title', 'description', 'order']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['part', 'title', 'description', 'order']

class LegalArticleForm(forms.ModelForm):
    class Meta:
        model = LegalArticle
        fields = ['section', 'title', 'reference_number', 'content', 'keywords', 'source_link', 'order', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
            'keywords': forms.TextInput(attrs={'placeholder': 'tax, banking, arbitration...'}),
        }
