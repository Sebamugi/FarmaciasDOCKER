#!/bin/bash
# Script para despliegue mediante archivo en Instancia 3

echo "Cargando la imagen Docker desde archivo..."
docker load < imagen_farmacia.tar

echo "Imagen cargada exitosamente"
echo "Ejecutando el contenedor..."
docker run -d -p 80:80 --name cliente_replica cliente-farmacia:v1

echo "Verificando que el contenedor esté corriendo..."
docker ps

echo "Contenedor ejecutándose en Instancia 3"
