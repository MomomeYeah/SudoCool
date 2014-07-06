from django import forms

class SolveForm(forms.Form):
    sudocoolData = forms.CharField(max_length=161)

class GetPuzzleForm(forms.Form):
    puzzleURL = forms.CharField()
