
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import InscriptionForm

def inscription(request):
    next_url = request.POST.get('next', request.GET.get('next', '/'))
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name} ! Votre compte a ete cree.')
            return redirect(next_url)
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form, 'next': next_url})

def connexion(request):
    next_url = request.GET.get('next', '/')
    if request.user.is_authenticated:
        return redirect(next_url)
    error = None
    username = ''
    if request.method == 'POST':
        next_url = request.POST.get('next', '/')
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            error = 'Identifiants incorrects.'
    from .forms import InscriptionForm
    return render(request, 'accounts/connexion.html', {
        'error': error, 'username': username,
        'next': next_url,
        'register_form': InscriptionForm(),
    })

def deconnexion(request):
    logout(request)
    return redirect('core:accueil')

def profil(request):
    from django.contrib.auth.decorators import login_required
    if not request.user.is_authenticated:
        return redirect('accounts:connexion')
    return render(request, 'accounts/profil.html')
