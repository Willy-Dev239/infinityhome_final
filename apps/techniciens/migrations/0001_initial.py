from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Technicien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('specialite', models.CharField(max_length=30, choices=[('electricien','Electricien'),('plombier','Plombier'),('ingenieur','Ingenieur en construction'),('soudeur','Soudeur'),('peintre','Peintre'),('menuisier','Menuisier')])),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True)),
                ('localite', models.CharField(max_length=100)),
                ('disponibilite', models.CharField(max_length=20, choices=[('disponible','Disponible'),('occupe','Occupe'),('conge','En conge')], default='disponible')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='techniciens/')),
                ('experience', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Technicien', 'verbose_name_plural': 'Techniciens', 'ordering': ['specialite', 'nom']},
        ),
    ]
