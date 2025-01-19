from minio import Minio
import os
from minio.error import S3Error
import sys

def main():
    grab_parquet()

def grab_parquet():
    """
    Charge uniquement les fichiers déjà téléchargés par `charger_data_taxi`
    depuis un dossier local vers un bucket MinIO.
    """
    # Initialisation du client MinIO
    client = Minio(
        "localhost:9000",  # Adresse du serveur MinIO
        access_key="minio-archi",  # Clé d'accès
        secret_key="minio123",     # Clé secrète
        secure=False               # False pour HTTP, True pour HTTPS
    )

    # Nom du bucket cible
    bucket_name = "taxi-data"

    # Vérification et création du bucket si nécessaire
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' créé avec succès.")
    else:
        print(f"Bucket '{bucket_name}' existe déjà.")

    # Dossier contenant les fichiers téléchargés par `charger_data_taxi`
    folder_path = os.path.abspath("../../data/raw")

    # Vérification si le dossier existe
    if not os.path.exists(folder_path):
        print(f"Le dossier local '{folder_path}' n'existe pas. Assurez-vous que `charger_data_taxi` a téléchargé les données.")
        return

    # Parcours des fichiers dans le dossier local
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Préparation des chemins local et distant
            file_path = os.path.join(root, file)  # Chemin absolu du fichier local
            object_name = os.path.relpath(file_path, folder_path)  # Nom relatif pour MinIO

            # Upload du fichier vers MinIO
            try:
                client.fput_object(
                    bucket_name=bucket_name,  # Bucket cible
                    object_name=object_name,  # Chemin/nouveau nom dans MinIO
                    file_path=file_path       # Chemin local du fichier
                )
                print(f"Fichier '{file}' chargé sous '{object_name}' dans le bucket '{bucket_name}'.")
            except S3Error as e:
                print(f"Erreur lors du chargement de '{file_path}': {e}")

if __name__ == '__main__':
    sys.exit(main())
