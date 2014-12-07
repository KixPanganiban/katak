from django import forms

class CorpusForm(forms.Form):
    corpusFile = forms.FileField(
        label="Select text file")