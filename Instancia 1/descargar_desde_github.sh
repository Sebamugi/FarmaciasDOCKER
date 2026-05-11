#!/bin/bash

# Script para descargar archivos específicos de la Instancia 1 desde GitHub
# Uso: ./descargar_desde_github.sh

echo "=== Descargando Instancia 1 desde GitHub ==="

# Crear directorio si no existe
mkdir -p Instancia1_Downloaded
cd Instancia1_Downloaded

# Base URL
BASE_URL="https://raw.githubusercontent.com/Sebamugi/FarmaciasDOCKER/main/Instancia%201"

# Archivos principales a descargar
echo "Descargando archivos principales..."
wget -q "$BASE_URL/server_api.py"
wget -q "$BASE_URL/requirements.txt"
wget -q "$BASE_URL/setup_database.sql"
wget -q "$BASE_URL/Dockerfile"
wget -q "$BASE_URL/docker-compose.yml"
wget -q "$BASE_URL/instalacion_dependencias.sh"

# Crear directorio templates
echo "Creando directorio templates..."
mkdir -p templates

# Descargar templates
echo "Descargando templates..."
wget -q "$BASE_URL/templates/base.html" -O templates/base.html
wget -q "$BASE_URL/templates/index.html" -O templates/index.html
wget -q "$BASE_URL/templates/farmacias.html" -O templates/farmacias.html
wget -q "$BASE_URL/templates/farmacia_form.html" -O templates/farmacia_form.html
wget -q "$BASE_URL/templates/estadisticas.html" -O templates/estadisticas.html

# Descargar configuración si existe
wget -q "$BASE_URL/configuracion_mariadb.cnf" -O configuracion_mariadb.cnf

echo "=== Descarga completada ==="
echo "Archivos descargados en: $(pwd)"
echo ""
echo "Para iniciar el servidor:"
echo "1. pip install -r requirements.txt"
echo "2. mysql -u root -p < setup_database.sql"
echo "3. python server_api.py"
echo ""
echo "Para usar Docker:"
echo "1. docker-compose up -d"


cd "c:/Users/Seba/Downloads/FarmaciasDocker/Instancia 1" ; chmod +x descargar_desde_github.sh