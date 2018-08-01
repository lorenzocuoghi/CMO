from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class DocumentForm(forms.Form):
    titolo = forms.CharField(max_length=200)
    content = forms.CharField(widget=CKEditorUploadingWidget())
