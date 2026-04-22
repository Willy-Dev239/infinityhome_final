
import functools
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from apps.demandes.models import Demande, Notification
from apps.techniciens.models import Technicien
from apps.accounts.models import Profil

def admin_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return redirect('dashboard:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:home')
    error = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username',''), password=request.POST.get('password',''))
        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('dashboard:home')
        error = 'Identifiants incorrects ou acces refuse.'
    return render(request, 'dashboard/login.html', {'error': error})

def admin_logout(request):
    logout(request)
    return redirect('dashboard:login')

@admin_required
def home(request):
    stats = {
        'total_demandes': Demande.objects.count(),
        'en_attente': Demande.objects.filter(statut='en_attente').count(),
        'en_cours': Demande.objects.filter(statut__in=['assignee','en_cours']).count(),
        'terminees': Demande.objects.filter(statut='terminee').count(),
        'total_techniciens': Technicien.objects.filter(actif=True).count(),
        'disponibles': Technicien.objects.filter(disponibilite='disponible', actif=True).count(),
        'total_clients': User.objects.filter(is_staff=False).count(),
    }
    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'demandes_recentes': Demande.objects.order_by('-date_creation')[:8],
        'techniciens_dispo': Technicien.objects.filter(disponibilite='disponible', actif=True)[:6],
    })

@admin_required
def demandes(request):
    statut = request.GET.get('statut', '')
    qs = Demande.objects.select_related('client','technicien').order_by('-date_creation')
    if statut:
        qs = qs.filter(statut=statut)
    return render(request, 'dashboard/demandes.html', {'demandes': qs, 'statut_actif': statut})



@admin_required
def demande_detail(request, pk):
    demande = get_object_or_404(Demande, pk=pk)

    # ✅ Correspondance entre type_travaux (Demande) et specialite (Technicien)
    # Adaptez selon vos vraies valeurs de Demande.TYPE_TRAVAUX
    MAPPING_SPECIALITE = {
        'electricite':  'electricien',
        'electrique':   'electricien',
        'electricien':  'electricien',
        'plomberie':    'plombier',
        'plombier':     'plombier',
        'construction': 'ingenieur',
        'genie_civil':  'ingenieur',
        'ingenieur':    'ingenieur',
        'soudure':      'soudeur',
        'soudeur':      'soudeur',
        'peinture':     'peintre',
        'peintre':      'peintre',
        'menuiserie':   'menuisier',
        'menuisier':    'menuisier',
    }

    specialite = MAPPING_SPECIALITE.get(
        demande.type_travaux,
        demande.type_travaux  # fallback si déjà identique
    )

    techniciens_dispo = Technicien.objects.filter(
        specialite=specialite,
        disponibilite='disponible',
        actif=True,
    ).order_by('nom')

    tous_techniciens = Technicien.objects.filter(
        specialite=specialite,
        actif=True,
    ).exclude(
        disponibilite='disponible'
    ).order_by('nom')

    return render(request, 'dashboard/demande_detail.html', {
        'demande': demande,
        'techniciens_dispo': techniciens_dispo,
        'tous_techniciens': tous_techniciens,
        'statuts': demande._meta.get_field('statut').choices,
    })
    
    
    
@admin_required
def assigner_technicien(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    if request.method == 'POST':
        tech_id = request.POST.get('technicien_id')
        date_intervention = request.POST.get('date_intervention')
        if tech_id:
            tech = get_object_or_404(Technicien, pk=tech_id)
            demande.technicien = tech
            demande.statut = 'assignee'
            if date_intervention:
                demande.date_intervention = date_intervention
            demande.save()
            # Notifier le client
            Notification.objects.create(
                utilisateur=demande.client,
                demande=demande,
                titre='Technicien assigne a votre demande',
                message=f'Bonjour {demande.client.first_name}, un technicien a ete assigne a votre demande "{demande.titre}". {tech.prenom} {tech.nom} ({tech.get_specialite_display()}) interviendra chez vous. Tel: {tech.telephone}',
            )
            # Email
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    f'Technicien assigne - Demande #{demande.id}',
                    f'Bonjour {demande.client.first_name},\n\n Un technicien a ete assigne a votre demande "{demande.titre}".\n\nTechnicien: {tech.prenom} {tech.nom}\nSpecialite: {tech.get_specialite_display()}\nTelephone: {tech.telephone}\n\nInfinity Home Rewire and Construction',
                    settings.DEFAULT_FROM_EMAIL,
                    [demande.client.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, f'Technicien {tech.nom_complet} assigne avec succes !')
    return redirect('dashboard:demande_detail', pk=pk)

@admin_required
def update_statut(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    if request.method == 'POST':
        new_statut = request.POST.get('statut')
        if new_statut:
            old_statut = demande.get_statut_display()
            demande.statut = new_statut
            demande.save()
            Notification.objects.create(
                utilisateur=demande.client,
                demande=demande,
                titre=f'Statut de votre demande mis a jour',
                message=f'Votre demande "{demande.titre}" est maintenant : {demande.get_statut_display()}.',
            )
            messages.success(request, 'Statut mis a jour.')
    return redirect('dashboard:demande_detail', pk=pk)

@admin_required
def techniciens(request):
    return render(request, 'dashboard/techniciens.html', {
        'techniciens': Technicien.objects.all().order_by('specialite','nom'),
    })

@admin_required
def technicien_add(request):
    from apps.techniciens.models import SPECIALITES, DISPONIBILITE
    if request.method == 'POST':
        try:
            t = Technicien(
                nom=request.POST['nom'],
                prenom=request.POST['prenom'],
                specialite=request.POST['specialite'],
                telephone=request.POST['telephone'],
                email=request.POST.get('email',''),
                localite=request.POST['localite'],
                disponibilite=request.POST.get('disponibilite','disponible'),
                experience=request.POST.get('experience',0),
            )
            if 'photo' in request.FILES:
                t.photo = request.FILES['photo']
            t.save()
            messages.success(request, f'Technicien {t.nom_complet} ajoute !')
            return redirect('dashboard:techniciens')
        except Exception as e:
            messages.error(request, f'Erreur: {e}')
    from apps.techniciens.models import SPECIALITES, DISPONIBILITE
    return render(request, 'dashboard/technicien_form.html', {
        'specialites': SPECIALITES, 'disponibilites': DISPONIBILITE
    })

@admin_required
def technicien_edit(request, pk):
    tech = get_object_or_404(Technicien, pk=pk)
    from apps.techniciens.models import SPECIALITES, DISPONIBILITE
    if request.method == 'POST':
        tech.nom = request.POST['nom']
        tech.prenom = request.POST['prenom']
        tech.specialite = request.POST['specialite']
        tech.telephone = request.POST['telephone']
        tech.email = request.POST.get('email','')
        tech.localite = request.POST['localite']
        tech.disponibilite = request.POST.get('disponibilite','disponible')
        tech.experience = request.POST.get('experience',0)
        tech.actif = 'actif' in request.POST
        if 'photo' in request.FILES:
            tech.photo = request.FILES['photo']
        tech.save()
        messages.success(request, f'Technicien {tech.nom_complet} mis a jour !')
        return redirect('dashboard:techniciens')
    return render(request, 'dashboard/technicien_form.html', {
        'tech': tech, 'specialites': SPECIALITES, 'disponibilites': DISPONIBILITE
    })

@admin_required
def clients(request):
    return render(request, 'dashboard/clients.html', {
        'clients': User.objects.filter(is_staff=False).order_by('-date_joined')
    })

@admin_required
def api_stats(request):
    return JsonResponse({
        'en_attente': Demande.objects.filter(statut='en_attente').count(),
    })


# ── CHAT ADMIN ──────────────────────────────────────────────────
@admin_required
def chat_admin(request):
    """Dashboard admin du groupe chat."""
    from apps.demandes.models import MessageChat
    messages_chat = MessageChat.objects.all().order_by('date_envoi')
    return render(request, 'dashboard/chat_admin.html', {'messages_chat': messages_chat})

@admin_required
def envoyer_message_admin(request):
    """Admin envoie un message dans le groupe."""
    import json
    from django.http import JsonResponse
    from django.views.decorators.http import require_POST
    from apps.demandes.models import MessageChat
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contenu = data.get('contenu','').strip()
            if not contenu:
                return JsonResponse({'ok':False,'error':'Message vide'})
            msg = MessageChat.objects.create(
                expediteur=request.user,
                contenu=contenu,
                is_admin=True,
            )
            return JsonResponse({
                'ok':True,'id':msg.id,
                'expediteur': msg.expediteur.get_full_name() or msg.expediteur.username,
                'contenu': msg.contenu,
                'date_envoi': msg.date_envoi.strftime('%H:%M'),
                'is_admin': True,'is_me':True,
            })
        except Exception as e:
            return JsonResponse({'ok':False,'error':str(e)})
    return JsonResponse({'ok':False})

@admin_required
def get_messages_admin(request):
    from django.http import JsonResponse
    from apps.demandes.models import MessageChat
    depuis_id = int(request.GET.get('depuis',0))
    msgs = MessageChat.objects.filter(id__gt=depuis_id).order_by('date_envoi')[:50]
    data = []
    for m in msgs:
        data.append({
            'id':m.id,
            'expediteur': m.expediteur.get_full_name() or m.expediteur.username,
            'username': m.expediteur.username,
            'contenu': m.contenu,
            'date_envoi': m.date_envoi.strftime('%H:%M'),
            'is_admin': m.is_admin,
            'is_me': m.expediteur == request.user,
        })
    return JsonResponse({'messages':data})
