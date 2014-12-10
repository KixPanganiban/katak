from django import forms

class CorpusForm(forms.Form):
    """
    Corpus file form. Just for adherence to Django conventions.
    """
    corpusFile = forms.FileField(
        label="Select text file")