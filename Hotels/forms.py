
from django import forms
from .models import Reserve_Room


class ReserveForm(forms.ModelForm):

    class Meta:
        model = Reserve_Room
        fields = ['Room_id', 'Rcheck_in', 'Rcheck_out']
