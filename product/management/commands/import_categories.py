import os
import csv
from django.core.management.base import BaseCommand
from product.models import Category

class Command(BaseCommand):
    help = 'Importe des catégories depuis un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin vers le fichier CSV')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        # Convertir le chemin relatif en absolu
        csv_file_path = os.path.abspath(csv_file_path)

        if not os.path.isfile(csv_file_path):
            self.stderr.write(self.style.ERROR(f"Le fichier {csv_file_path} est introuvable ou n'est pas un fichier valide."))
            return

        self.stdout.write(self.style.SUCCESS(f"Chargement du fichier {csv_file_path}..."))

        try:
            with open(csv_file_path, mode='r', encoding='latin1') as file:
                reader = csv.DictReader(file, delimiter=';')

                # Vérification des colonnes attendues
                self.stdout.write(self.style.SUCCESS("Vérification des colonnes..."))
                self.stdout.write(self.style.SUCCESS(f"Colonnes trouvées : {reader.fieldnames}"))

                if not all(col in reader.fieldnames for col in ['CL_No', 'CL_Intitule', 'CL_NoParent']):
                    self.stderr.write(self.style.ERROR("Le fichier CSV ne contient pas toutes les colonnes requises : 'CL_No', 'CL_Intitule', 'CL_NoParent'."))
                    return

                self.stdout.write(self.style.SUCCESS("Fichier chargé avec succès."))
                self.stdout.write(self.style.SUCCESS(f"Nombre de lignes : {sum(1 for row in reader)}"))

                # Revenir au début du fichier pour réinitialiser le lecteur
                file.seek(0)
                reader = csv.DictReader(file, delimiter=';')

                # Dictionnaire pour stocker les catégories créées
                categories = {}

                for row in reader:
                    cl_no = int(row['CL_No'])
                    cl_intitule = row['CL_Intitule']
                    cl_no_parent = int(row['CL_NoParent'])

                    # Vérifier si la catégorie parent existe déjà
                    parent = None
                    if cl_no_parent != 0:
                        parent = categories.get(cl_no_parent)

                    # Créer la catégorie avec l'ID spécifique
                    category, created = Category.objects.update_or_create(
                        id=cl_no,  # Utiliser CL_No comme ID
                        defaults={'name': cl_intitule, 'parent': parent}  # Mettre à jour ou créer avec ces valeurs
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Catégorie {cl_intitule} (ID: {cl_no}) enregistrée avec succès."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Catégorie {cl_intitule} (ID: {cl_no}) déjà présente dans la base."))

                    # Ajouter la catégorie au dictionnaire
                    categories[cl_no] = category

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Le fichier {csv_file_path} est introuvable."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Une erreur est survenue : {str(e)}"))
