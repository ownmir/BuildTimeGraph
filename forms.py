from django import forms


class PauseForm(forms.Form):
    pause = forms.IntegerField(min_value=3, max_value=8)
