from django import forms

from poll.models import ScoreRecord

class ScoreRecordForm(forms.ModelForm):
    class Meta:
        model = ScoreRecord
        fields = ('email',)

        widgets = {
            'text' : forms.fields.TextInput(attrs={
                'id' : 'email_input_id',
            })
        }

    def save(self, score):
        self.instance.score = score
        return super().save()
