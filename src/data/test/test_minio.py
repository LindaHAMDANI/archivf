import boto3

# Configuration de MinIO
endpoint_url = "http://localhost:9000/"
access_key = "minio-archi"
secret_key = "minio123"

# Créer le client S3
s3 = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# Lister les buckets
try:
    response = s3.list_buckets()
    print("Buckets disponibles dans MinIO :")
    for bucket in response['Buckets']:
        print(f"  - {bucket['Name']}")
except Exception as e:
    print("Erreur lors de la connexion à MinIO :", e)
