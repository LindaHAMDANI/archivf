from minio import Minio
import urllib.request
import pandas as pd
import sys
import os
import urllib.request
import re
from bs4 import BeautifulSoup
from minio import Minio
from minio.error import S3Error

def main():
    grab_data()
    grab_latest_data()
    write_data_minio()

# Fonction qui récupère les data sur le site de NYC.gov 
# Ici uniquement janvier car les téléchargements sont longs

def grab_data() -> None:
    """Récupère les données de New York Yellow Taxi pour janvier 2024

    Cette méthode télécharge le fichier des trajets des Yellow Taxi de janvier 2024 au format Parquet.
    Le fichier est enregistré dans le dossier "../../data/raw".
    """
    base_url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    folder_path = "C:/Users/33656/archivf/archivf/data/raw"
    
    # Création du dossier s'il n'existe pas
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Téléchargement du contenu de la page
    print("Récupération du lien de téléchargement pour janvier 2024...")
    try:
        with urllib.request.urlopen(base_url) as response:
            page_content = response.read()
    except Exception as e:
        print(f"Erreur lors du téléchargement de la page principale : {e}")
        return

    # Parsing du contenu de la page avec BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    pattern = re.compile(r'yellow_tripdata_2024-01\.parquet')

    # Trouver le lien du fichier Parquet pour janvier 2024
    link = None
    for a in soup.find_all('a', href=True):
        if pattern.search(a['href']):
            link = a['href']
            break
    
    # Affiche le lien du fichier téléchargé
    print("Lien du fichier :", link)
    print("Chemin du dossier de destination :", folder_path)
    
    if not link:
        print("Le fichier Parquet pour janvier 2024 n'a pas été trouvé.")
        return

    # Télécharger le fichier
    file_name = link.split('/')[-1]
    file_path = os.path.join(folder_path, file_name)

    print("Chemin complet du fichier :", file_path)
    print(f"Téléchargement de {file_name}...")
    try:
        urllib.request.urlretrieve(link, file_path)
        print(f"{file_name} téléchargé avec succès.")
    except Exception as e:
        print(f"Échec du téléchargement de {file_name} : {e}")

# # Fonction qui récupère toutes les data de tous les mois de l'année 2024
# def grab_data() -> None:
#     """Récupère les données de New York Yellow Taxi pour tous les mois de 2024
# 
#     Cette méthode télécharge les fichiers des trajets des Yellow Taxi au format Parquet pour tous les mois de l'année 2024.
#     Les fichiers sont enregistrés dans le dossier "../../data/raw".
#     """
#     base_url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
#     folder_path = os.path.abspath("../../data/raw")  # Utilisation du chemin absolu
# 
#     # Création du dossier s'il n'existe pas
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
# 
#     # Téléchargement du contenu de la page
#     print("Récupération des liens de téléchargement pour les mois de l'année 2024...")
#     try:
#         with urllib.request.urlopen(base_url) as response:
#             page_content = response.read()
#     except Exception as e:
#         print(f"Erreur lors du téléchargement de la page principale : {e}")
#         return
# 
#     # Parsing du contenu de la page avec BeautifulSoup
#     soup = BeautifulSoup(page_content, 'html.parser')
#     pattern = re.compile(r'yellow_tripdata_2024-\d{2}\.parquet')
# 
#     # Trouver tous les liens des fichiers Parquet pour 2024
#     links = [a['href'] for a in soup.find_all('a', href=True) if pattern.search(a['href'])]
# 
#     if not links:
#         print("Aucun fichier Parquet trouvé pour l'année 2024.")
#         return
# 
#     # Téléchargement de chaque fichier trouvé
#     for link in links:
#         file_name = link.split('/')[-1]
#         file_path = os.path.join(folder_path, file_name)
# 
#         print(f"Téléchargement de {file_name}...")
#         try:
#             urllib.request.urlretrieve(link, file_path)
#             print(f"{file_name} téléchargé avec succès.")
#         except Exception as e:
#             print(f"Échec du téléchargement de {file_name} : {e}")

def grab_latest_data() -> None:
    """Récupère les données de New York Yellow Taxi pour le mois le plus récent disponible

    Cette méthode télécharge le fichier des trajets des Yellow Taxi du mois le plus récent au format Parquet.
    Le fichier est enregistré dans le dossier "../../data/raw".
    """
    base_url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    folder_path = "C:/Users/33656/archivf/archivf/data/raw"

    # Téléchargement du contenu de la page
    print("Récupération du lien de téléchargement pour le mois le plus récent...")
    try:
        with urllib.request.urlopen(base_url) as response:
            page_content = response.read()
    except Exception as e:
        print(f"Erreur lors du téléchargement de la page principale : {e}")
        return

    # Parsing du contenu de la page avec BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    pattern = re.compile(r'yellow_tripdata_\d{4}-\d{2}\.parquet')

    # Trouver tous les liens des fichiers Parquet
    links = [a['href'] for a in soup.find_all('a', href=True) if pattern.search(a['href'])]

    if not links:
        print("Aucun fichier Parquet trouvé.")
        return

    # Trier les liens pour trouver le plus récent (basé sur l'année et le mois dans le nom du fichier)
    links.sort(reverse=True)
    latest_link = links[0]  # Le plus récent

    # Télécharger le fichier
    file_name = latest_link.split('/')[-1]
    file_path = os.path.join(folder_path, file_name)

    print(f"Téléchargement de {file_name}...")
    try:
        urllib.request.urlretrieve(latest_link, file_path)
        print(f"{file_name} téléchargé avec succès.")
    except Exception as e:
        print(f"Échec du téléchargement de {file_name} : {e}")

def write_data_minio():
    """
    This method put all Parquet files into Minio
    Ne pas faire cette méthode pour le moment
    """
    pass

if __name__ == '__main__':
    sys.exit(main())
