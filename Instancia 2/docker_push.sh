#!/bin/bash
# Script para subir la imagen a Docker Hub (opcional)

echo "Iniciando sesión en Docker Hub..."
docker login

echo "Tageando la imagen para Docker Hub..."
docker tag cliente-farmacia:v1 Sebamugi/cliente-farmacia:v1

echo "Subiendo la imagen a Docker Hub..."
docker push Sebamugi/cliente-farmacia:v1

echo "Imagen subida exitosamente a Docker Hub"
echo "Para descargar en la Instancia 3:"
echo "docker run -d -p 80:80 --name cliente_replica Sebamugi/cliente-farmacia:v1"
