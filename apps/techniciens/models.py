
from django.db import models

SPECIALITES = [
    ('electricien',   'Electricien'),
    ('plombier',      'Plombier'),
    ('ingenieur',     'Ingenieur en construction'),
    ('soudeur',       'Soudeur'),
    ('peintre',       'Peintre'),
    ('menuisier',     'Menuisier'),
]

DISPONIBILITE = [
    ('disponible',    'Disponible'),
    ('occupe',        'Occupe'),
    ('conge',         'En conge'),
]

class Technicien(models.Model):
    nom         = models.CharField(max_length=100)
    prenom      = models.CharField(max_length=100)
    specialite  = models.CharField(max_length=30, choices=SPECIALITES)
    telephone   = models.CharField(max_length=20)
    email       = models.EmailField(blank=True)
    localite    = models.CharField(max_length=100)
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE, default='disponible')
    photo       = models.ImageField(upload_to='techniciens/', blank=True, null=True)
    experience  = models.PositiveIntegerField(default=0, help_text='Annees experience')
    actif       = models.BooleanField(default=True)
    date_ajout  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Technicien'
        verbose_name_plural = 'Techniciens'
        ordering = ['specialite', 'nom']

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_specialite_display()}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
