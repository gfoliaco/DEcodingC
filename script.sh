#!/bin/bash

# Define las variables de entorno
export GCP_REGION="us-central1"
export GCP_PROJECT_ID="unified-era-355307"

# Construir la imagen Docker
sudo docker build -t database_app .

# Etiquetar la imagen Docker para Google Container Registry
sudo docker tag database_app gcr.io/$GCP_PROJECT_ID/databaseapp:v1

# Subir la imagen Docker a Google Container Registry
sudo docker push gcr.io/$GCP_PROJECT_ID/databaseapp:v1

# Agregar etiquetas a la imagen en Google Container Registry
gcloud container images add-tag gcr.io/$GCP_PROJECT_ID/databaseapp:v1 gcr.io/$GCP_PROJECT_ID/databaseapp:public --quiet

# Inicializar Terraform
terraform init

# Aplicar Terraform
terraform apply
