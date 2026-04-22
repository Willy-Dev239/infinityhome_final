
from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['type_travaux','titre','description','localite','adresse','urgence','photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
            'adresse': forms.Textarea(attrs={'rows':2}),
        }
