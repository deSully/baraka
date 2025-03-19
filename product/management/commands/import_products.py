import os
import csv
from django.core.management.base import BaseCommand
from product.models import Product, Category, ProductPrice

class Command(BaseCommand):
    help = 'Importe des articles depuis un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin vers le fichier CSV des articles')

    def convert_stock(self, value):
        try:
            # Supprimer les espaces et les virgules
            value = value.strip().replace(',', '.')
            
            # Essayer de convertir en entier
            return int(value)
        except ValueError:
            try:
                # Si une erreur se produit, essayer de convertir en float
                return float(value)
            except ValueError:
                # Si ça échoue encore, on retourne 0 par défaut
                return 0

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
                if not all(col in reader.fieldnames for col in ['AR_Ref', 'AR_Design', 'CATEGORIE', 'STOCK', 'PV_CAT_01', 'PV_CAT_02', 'PV_CAT_03', 'PV_CAT_04', 'PV_CAT_05', 'PV_CAT_06', 'PV_CAT_07', 'PV_CAT_09', 'PV_CAT_10']):
                    self.stderr.write(self.style.ERROR("Le fichier CSV ne contient pas toutes les colonnes requises."))
                    return

                self.stdout.write(self.style.SUCCESS("Fichier chargé avec succès."))

                # Revenir au début du fichier pour réinitialiser le lecteur
                file.seek(0)
                reader = csv.DictReader(file, delimiter=';')

                for row in reader:
                    # Récupérer ou créer la catégorie
                    try:
                        category = Category.objects.get(id=row['CATEGORIE'])
                    except Category.DoesNotExist:
                        self.stderr.write(self.style.ERROR(f"Catégorie avec ID {row['CATEGORIE']} non trouvée."))
                        continue

                    # Créer ou récupérer le produit

                    stock = 0

                    try:
                        # Supprimer les espaces et les virgules
                        value = row['STOCK'].strip().replace(',', '.')
                        
                        # Essayer de convertir en entier
                        stock =  int(value)
                    except ValueError:
                        try:
                            # Si une erreur se produit, essayer de convertir en float
                            stock =  float(value)
                        except ValueError:
                            # Si ça échoue encore, on retourne 0 par défaut
                            return 0
                    
                    product, created = Product.objects.update_or_create(
                        reference=row['AR_Ref'],  # Utiliser AR_Ref comme identifiant unique
                        defaults={'name': row['AR_Design'], 'stock': stock, 'category': category}
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Produit {product.name} (Référence: {product.reference}) ajouté."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Produit {product.name} (Référence: {product.reference}) déjà existant."))

                    # Ajouter les prix
                    for i in range(1, 11):  # PV_CAT_01 à PV_CAT_10
                        price_key = f'PV_CAT_0{i}'
                        price_value = row.get(price_key)
                        if price_value:
                            price_value = float(price_value.replace(',', '.'))  # Remplacer la virgule par un point pour les prix
                            ProductPrice.objects.create(
                                product=product,
                                criterion=f'PV_CAT_{i}',
                                price=price_value
                            )
                            self.stdout.write(self.style.SUCCESS(f"Prix pour {product.name} (Référence: {product.reference}) ajouté : {price_value}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Le fichier {csv_file_path} est introuvable."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Une erreur est survenue : {str(e)}"))
