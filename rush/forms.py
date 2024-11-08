from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from .models import Filing, Rushee, Signin
from django.contrib.auth import get_user_model


# Form for filing on a rushee
class FilingForm(forms.Form):
    CHOICES = (('x', 'No Filing'),) + Filing.FILING_TYPES
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='', initial='x')


# Form for adding new actives
class NewActiveForm(forms.Form):
    actives = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter one set of initials per line', 'rows': 5}),
        label='New Actives', required=False, )


# Form for modifying active traits (checkboxes for staff, delete, and reset password)
class ModifyActivesForm(forms.Form):
    def __init__(self, actives, user, *args, **kwargs):
        super(ModifyActivesForm, self).__init__(*args, **kwargs)
        for i in actives:
            active = i.username
            self.fields[active + 'Staff'] = forms.BooleanField(initial=i.is_staff, label=active.upper(),
                                                               label_suffix='', disabled=(i == user), required=False)
            self.fields[active + 'Delete'] = forms.BooleanField(initial=False, disabled=(i == user), required=False)
            self.fields[active + 'Password'] = forms.BooleanField(initial=False, disabled=(i == user), required=False)


# Form for adding rushees
class AddRusheesForm(forms.Form):
    rushees = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter one name per line',
        'rows': 5}), label='New Rushees', required=False, )


# Form for modifying a rushee
class ModifyRusheeForm(forms.ModelForm):
    class Meta:
        model = Rushee
        fields = ['name', 'status', 'bidder', 'pronouns', 'dorm', 'email', 'discord', 'phone', 'last_contact', 'comments']


# Form for modifying autobid settings
class SettingsForm(forms.Form):
    b = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))
    n = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))
    w = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))
    f = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'style': 'width: 5ch;'}))


# Form for deleting rushees or filings
class DeleteForm(forms.Form):
    filings = forms.BooleanField(label="Delete All Filings", required=False)
    rushees = forms.BooleanField(label="Delete All Rushees", required=False)
    signins = forms.BooleanField(label="Delete All Sign-ins", required=False)


# Form for filing as a specific user
class FileAsUserForm(forms.Form):
    User = get_user_model()
    user = forms.ModelChoiceField(User.objects.all())
    rushee = forms.ModelChoiceField(Rushee.objects.all())
    CHOICES = (('x', 'No Filing'),) + Filing.FILING_TYPES
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Filing', initial='x')


# Form for merging two rushees
class MergeForm(forms.Form):
    r1 = forms.ModelChoiceField(Rushee.objects.all(), label='Rushee 1')
    r2 = forms.ModelChoiceField(Rushee.objects.all(), label='Rushee 2')

    def clean(self):
        cleaned_data = super().clean()
        r1 = cleaned_data.get("r1")
        r2 = cleaned_data.get("r2")

        if r1 == r2:
            raise ValidationError('Rushees must be different.')


# Form for setting Discord username
class DiscordForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 30ch;'}), label='User ID')


# Sign-in form
class SigninForm(forms.ModelForm):
    class Meta:
        model = Signin
        fields = ['name', 'email', 'heard']
        labels = {
            'heard': 'How did you hear about this event'
        }


# Set of filing forms
FilingFormSet = formset_factory(FilingForm, extra=0)
