from django import forms


class DocumentForm(forms.Form):
    titolo = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea(), required=False)
