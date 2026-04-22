
from django.shortcuts import render
from .models import Technicien, SPECIALITES

def liste_techniciens(request):
    specialite = request.GET.get('specialite', '')
    techniciens = Technicien.objects.filter(actif=True)
    if specialite:
        techniciens = techniciens.filter(specialite=specialite)
    return render(request, 'techniciens/liste.html', {
        'techniciens': techniciens,
        'specialites': SPECIALITES,
        'specialite_active': specialite,
    })
