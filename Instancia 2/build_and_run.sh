#!/bin/bash
# Script para construir y ejecutar el contenedor Docker de la Instancia 2

echo "Instalando Docker..."
sudo dnf update -y
sudo dnf install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER && newgrp docker

echo "Construyendo la imagen Docker..."
docker build -t cliente-farmacia:v1 .

echo "Ejecutando el contenedor..."
docker run -d -p 80:80 --name app_cliente cliente-farmacia:v1

echo "Verificando que el contenedor esté corriendo..."
docker ps

echo "Para probar el funcionamiento:"
echo "curl 'http://localhost/consultar?comuna=Coronel&abiertas=true'"
