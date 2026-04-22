
from django.shortcuts import render
from apps.techniciens.models import Technicien, SPECIALITES

def accueil(request):
    techniciens_par_specialite = []
    for code, label in SPECIALITES:
        techs = Technicien.objects.filter(specialite=code, actif=True, disponibilite='disponible')[:3]
        techniciens_par_specialite.append({
            'code': code, 'label': label, 'techniciens': techs,
            'count': Technicien.objects.filter(specialite=code, actif=True).count(),
        })
    return render(request, 'core/accueil.html', {
        'specialites': techniciens_par_specialite,
        'total_techniciens': Technicien.objects.filter(actif=True).count(),
    })

def nos_services(request):
    return render(request, 'core/services.html', {'specialites': SPECIALITES})

def a_propos(request):
    return render(request, 'core/a_propos.html')
def surveillance(request):
    techniciens = Technicien.objects.filter(actif=True, specialite='surveillance')
    return render(request, 'core/surveillance.html', {'techniciens': techniciens})
def contact(request):
    from django.contrib import messages
    if request.method == 'POST':
        messages.success(request, 'Votre message a ete envoye. Nous vous repondrons bientot !')
    return render(request, 'core/contact.html')
