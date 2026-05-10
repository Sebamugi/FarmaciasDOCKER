#!/bin/bash
# Script para despliegue mediante Docker Hub en Instancia 3

echo "Descargando y ejecutando el contenedor desde Docker Hub..."
# Reemplaza 'usuario' por el nombre de cuenta de tu compañero
docker run -d -p 80:80 --name cliente_replica Sebamugi/cliente-farmacia:v2

echo "Contenedor descargado y ejecutado"
echo "Docker detectará que no tienes la imagen localmente, la descargará de internet y la pondrá en marcha automáticamente."

echo "Verificando que el contenedor esté corriendo..."
docker ps
