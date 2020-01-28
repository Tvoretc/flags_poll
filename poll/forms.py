from django import forms

from poll.models import ScoreRecord

class ScoreRecordForm(forms.Form):
    email = forms.EmailField()
