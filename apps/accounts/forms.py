
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profil

class InscriptionForm(UserCreationForm):
    email      = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=50, required=True, label='Prenom')
    last_name  = forms.CharField(max_length=50, required=True, label='Nom')
    telephone  = forms.CharField(max_length=20, required=False, label='Telephone')
    localite   = forms.CharField(max_length=100, required=True, label='Localite / Quartier')
    adresse    = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), required=False, label='Adresse complete')
    
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profil.objects.create(
                user=user,
                telephone=self.cleaned_data.get('telephone',''),
                localite=self.cleaned_data.get('localite',''),
                adresse=self.cleaned_data.get('adresse',''),
            )
        return user

