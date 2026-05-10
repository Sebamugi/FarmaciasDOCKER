#!/bin/bash
# Script de preparación para Instancia 3

echo "Instalando Docker en Instancia 3..."
sudo dnf update -y
sudo dnf install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER && newgrp docker

echo "Docker instalado y configurado en Instancia 3"
echo "Listo para recibir la imagen de la Instancia 2"
