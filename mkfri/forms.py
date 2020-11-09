from django import forms

class HelloForm(forms.Form):
  id = forms.IntegerField(label='id')
  