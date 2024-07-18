from django import forms
from django.forms import formset_factory

from .models import Filing, Rushee


class FilingForm(forms.Form):
    CHOICES = (('x', 'No Filing'),) + Filing.FILING_TYPES
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='', initial='x')


class NewActiveForm(forms.Form):
    actives = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter one set of initials per line', 'rows': 5}),
        label='New Actives', required=False, )


class ModifyActivesForm(forms.Form):
    def __init__(self, actives, user, *args, **kwargs):
        super(ModifyActivesForm, self).__init__(*args, **kwargs)
        for i in actives:
            active = i.username
            self.fields[active + 'Staff'] = forms.BooleanField(initial=i.is_staff, label=active.upper(),
                                                               label_suffix='', disabled=(i == user), required=False)
            self.fields[active + 'Delete'] = forms.BooleanField(initial=False, disabled=(i == user), required=False)
            self.fields[active + 'Password'] = forms.BooleanField(initial=False, disabled=(i == user), required=False)


class AddRusheesForm(forms.Form):
    rushees = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter one name per line',
        'rows': 5}), label='New Rushees', required=False, )


class ModifyRusheeForm(forms.ModelForm):
    class Meta:
        model = Rushee
        fields = ['name', 'status', 'bidder', 'dorm', 'email', 'discord', 'phone', 'comments']


class SettingsForm(forms.Form):
    b = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))
    n = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))
    w = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))
    f = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))


class DeleteForm(forms.Form):
    filings = forms.BooleanField(label="Delete All Filings", required=False)
    rushees = forms.BooleanField(label="Delete All Rushees", required=False)


FilingFormSet = formset_factory(FilingForm, extra=0)
