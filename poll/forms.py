from django import forms

from poll.models import ScoreRecord

class ScoreRecordForm(forms.Form):
    email = forms.EmailField()

    # widgets = {
    #     'email' : forms.fields.TextInput(attrs={
    #         'id' : 'id_email_input',
    #     })
    # }
