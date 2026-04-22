
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Demande, Notification
from .forms import DemandeForm

@login_required
def nouvelle_demande(request):
    if request.method == 'POST':
        form = DemandeForm(request.POST, request.FILES)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.client = request.user
            demande.save()
            # Notification in-site
            Notification.objects.create(
                utilisateur=request.user,
                demande=demande,
                titre='Demande envoyee avec succes',
                message=f'Votre demande #{demande.id} "{demande.titre}" a ete recue. Un technicien vous sera assigne bientot.',
            )
            # Email au client
            try:
                send_mail(
                    f'Demande #{demande.id} recue - Infinity Home',
                    f'Bonjour {request.user.first_name},\n\nVotre demande "{demande.titre}" a ete recue.\nNous allons vous assigner un technicien disponible.\n\nInfinity Home Rewire and Construction',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                )
            except:
                pass
            messages.success(request, f'Demande #{demande.id} envoyee ! Vous serez notifie quand un technicien sera assigne.')
            return redirect('demandes:mes_demandes')
    else:
        form = DemandeForm()
    return render(request, 'demandes/nouvelle_demande.html', {'form': form})

@login_required
def mes_demandes(request):
    demandes = Demande.objects.filter(client=request.user)
    return render(request, 'demandes/mes_demandes.html', {'demandes': demandes})

@login_required
def detail_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk, client=request.user)
    return render(request, 'demandes/detail_demande.html', {'demande': demande})

@login_required
def notifications(request):
    notifs = Notification.objects.filter(utilisateur=request.user)
    notifs.filter(lue=False).update(lue=True)
    return render(request, 'demandes/notifications.html', {'notifications': notifs})

@login_required
def notif_count(request):
    from django.http import JsonResponse
    count = Notification.objects.filter(utilisateur=request.user, lue=False).count()
    return JsonResponse({'count': count})


# ─── CHAT VIEWS ──────────────────────────────────────────────────
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import MessageChat

@login_required
def chat_client(request):
    """Vue chat pour le client — groupe global avec admin."""
    messages_chat = list(
        MessageChat.objects.all().order_by('date_envoi')[:100]
    )
    return render(request, 'demandes/chat.html', {'messages_chat': messages_chat})

@login_required
@require_POST
def envoyer_message(request):
    """Envoyer un message dans le groupe chat."""
    try:
        data = json.loads(request.body)
        contenu = data.get('contenu', '').strip()
        if not contenu or len(contenu) > 1000:
            return JsonResponse({'ok': False, 'error': 'Message invalide'})
        msg = MessageChat.objects.create(
            expediteur=request.user,
            contenu=contenu,
            is_admin=request.user.is_staff or request.user.is_superuser,
        )
        return JsonResponse({
            'ok': True,
            'id': msg.id,
            'expediteur': msg.expediteur.get_full_name() or msg.expediteur.username,
            'contenu': msg.contenu,
            'date_envoi': msg.date_envoi.strftime('%H:%M'),
            'is_admin': msg.is_admin,
            'is_me': True,
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def get_messages(request):
    """Récupérer les nouveaux messages (polling)."""
    depuis_id = int(request.GET.get('depuis', 0))
    msgs = MessageChat.objects.filter(id__gt=depuis_id).order_by('date_envoi')[:50]
    data = []
    for m in msgs:
        data.append({
            'id': m.id,
            'expediteur': m.expediteur.get_full_name() or m.expediteur.username,
            'username': m.expediteur.username,
            'contenu': m.contenu,
            'date_envoi': m.date_envoi.strftime('%H:%M'),
            'is_admin': m.is_admin,
            'is_me': m.expediteur == request.user,
        })
    return JsonResponse({'messages': data})
