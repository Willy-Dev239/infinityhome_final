# 🏗️ Infinity Home Rewire & Construction
### Application Web Django — Gestion de demandes d'intervention

---

## 🚀 Installation

### 1. Créer la base MySQL
```sql
CREATE DATABASE infinityhome_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'infinity'@'localhost' IDENTIFIED BY 'infinity123';
GRANT ALL PRIVILEGES ON infinityhome_db.* TO 'infinity'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Modifier `infinity/settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'infinityhome_db',
        'USER': 'infinity',
        'PASSWORD': ''infinity123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Installer et migrer
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## ⚠️ IMPORTANT — Changer le numéro WhatsApp

Remplacez `+257 79 000 000` et `25779000000` dans :
- `templates/base/base.html` (bouton flottant + sidebar)
- `templates/demandes/chat.html` (carte contact)
- `templates/core/contact.html`
- `templates/core/accueil.html`

---

## 📱 Fonctionnalités

### Côté Client
- **Tableau de bord** avec accès rapide à toutes les fonctions
- **Menu vertical sidebar** — navigation intuitive
- **Nouvelle demande** d'intervention (type, description, photo)
- **Suivi en temps réel** avec barre de progression
- **Groupe Chat** style WhatsApp avec l'admin
- **Notifications** push pour chaque mise à jour
- **WhatsApp flottant** pour contacter l'admin directement
- **Profil** client complet

### Côté Admin (`/dashboard/`)
- **Tableau de bord** avec statistiques
- **Gestion des demandes** — assigner technicien, changer statut
- **Groupe Chat Admin** — répondre aux clients en temps réel
- **Gestion des techniciens** — ajouter, modifier, disponibilité
- **Liste des clients**

---

## 🏗️ Structure
```
infinity/
├── apps/
│   ├── accounts/    ← Inscription, connexion, profil
│   ├── core/        ← Pages publiques (accueil, services, contact)
│   ├── dashboard/   ← Interface admin
│   ├── demandes/    ← Demandes, notifications, chat
│   └── techniciens/ ← Gestion techniciens
├── templates/       ← Tous les templates HTML
├── infinity/        ← Settings, URLs
└── requirements.txt
```

## 🌐 URLs
| URL | Description |
|-----|-------------|
| `/` | Accueil (ou dashboard si connecté) |
| `/accounts/connexion/` | Page de connexion |
| `/accounts/inscription/` | Inscription |
| `/demandes/nouvelle/` | Nouvelle demande |
| `/demandes/chat/` | Groupe Chat |
| `/dashboard/` | Admin dashboard |
| `/dashboard/chat/` | Chat admin |
