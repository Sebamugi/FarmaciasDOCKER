#!/bin/bash
# Script para exportar la imagen Docker a un archivo (método manual)

echo "Exportando la imagen Docker a archivo..."
docker save cliente-farmacia:v1 > imagen_farmacia.tar

echo "Imagen exportada como imagen_farmacia.tar"
echo "Transfiera este archivo a la Instancia 3 usando scp:"
echo "scp imagen_farmacia.tar usuario@ip_instancia_3:/home/usuario/"
echo ""
echo "En la Instancia 3, ejecute:"
echo "docker load < imagen_farmacia.tar"
echo "docker run -d -p 80:80 --name cliente_replica cliente-farmacia:v1"
