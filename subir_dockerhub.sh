#!/bin/bash

# Script para subir imágenes a Docker Hub
# Uso: ./subir_dockerhub.sh

echo "=== Subiendo imágenes a Docker Hub ==="

# Variables
DOCKERHUB_USER="sebamugi"
SERVER_IMAGE="farmacias-server"
CLIENT_IMAGE="farmacias-client"

# Verificar login a Docker Hub
echo "Verificando login a Docker Hub..."
if ! docker info | grep -q "Username.*$DOCKERHUB_USER"; then
    echo "Por favor, inicia sesión en Docker Hub:"
    echo "docker login"
    read -p "Presiona Enter después de hacer login..."
fi

# Construir imagen del servidor (Instancia 1)
echo "Construyendo imagen del servidor..."
cd "Instancia 1"
docker build -t $DOCKERHUB_USER/$SERVER_IMAGE:latest .
docker tag $DOCKERHUB_USER/$SERVER_IMAGE:latest $DOCKERHUB_USER/$SERVER_IMAGE:$(date +%Y%m%d)

# Construir imagen del cliente (Instancia 2)
echo "Construyendo imagen del cliente..."
cd "../Instancia 2"
docker build -t $DOCKERHUB_USER/$CLIENT_IMAGE:latest .
docker tag $DOCKERHUB_USER/$CLIENT_IMAGE:latest $DOCKERHUB_USER/$CLIENT_IMAGE:$(date +%Y%m%d)

# Subir imágenes
echo "Subiendo imagen del servidor..."
docker push $DOCKERHUB_USER/$SERVER_IMAGE:latest
docker push $DOCKERHUB_USER/$SERVER_IMAGE:$(date +%Y%m%d)

echo "Subiendo imagen del cliente..."
docker push $DOCKERHUB_USER/$CLIENT_IMAGE:latest
docker push $DOCKERHUB_USER/$CLIENT_IMAGE:$(date +%Y%m%d)

echo "=== Imágenes subidas exitosamente ==="
echo ""
echo "Para usar las imágenes:"
echo "Servidor: docker run -p 5000:5000 $DOCKERHUB_USER/$SERVER_IMAGE:latest"
echo "Cliente: docker run -p 80:80 $DOCKERHUB_USER/$CLIENT_IMAGE:latest"
echo ""
echo "Para descargar:"
echo "Servidor: docker pull $DOCKERHUB_USER/$SERVER_IMAGE:latest"
echo "Cliente: docker pull $DOCKERHUB_USER/$CLIENT_IMAGE:latest"
