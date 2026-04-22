from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('techniciens', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('type_travaux', models.CharField(max_length=30, choices=[('electricite','Electricite'),('plomberie','Plomberie'),('construction','Construction'),('soudure','Soudure'),('peinture','Peinture'),('menuiserie','Menuiserie'),('autre','Autre')])),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('localite', models.CharField(max_length=200)),
                ('adresse', models.TextField()),
                ('urgence', models.CharField(max_length=20, choices=[('normale','Normale'),('urgente','Urgente'),('critique','Critique')], default='normale')),
                ('statut', models.CharField(max_length=20, choices=[('en_attente','En attente'),('assignee','Assignee'),('en_cours','En cours'),('terminee','Terminee'),('annulee','Annulee')], default='en_attente')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='demandes/')),
                ('notes_admin', models.TextField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('date_intervention', models.DateField(null=True, blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='auth.user')),
                ('technicien', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demandes', to='techniciens.technicien')),
            ],
            options={'verbose_name': 'Demande', 'verbose_name_plural': 'Demandes', 'ordering': ['-date_creation']},
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('lue', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('demande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='demandes.demande')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='auth.user')),
            ],
            options={'ordering': ['-date']},
        ),
    ]
