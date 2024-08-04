from django import forms

class SnippetForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Enter your snippet')
    key = forms.CharField(max_length=32, required=False, label='Secret Key (optional)', help_text='Used to encrypt your snippet')
