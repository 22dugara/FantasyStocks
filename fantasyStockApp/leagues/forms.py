from django import forms
from .models import League

class CreateLeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'description', 'key']

class JoinLeagueForm(forms.Form):
    league = forms.ModelChoiceField(queryset=League.objects.all())
    key = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super().clean()
        league = cleaned_data.get("league")
        key = cleaned_data.get("key")

        if league and key:
            if league.key != key:
                raise forms.ValidationError("The key is incorrect.")
        return cleaned_data
