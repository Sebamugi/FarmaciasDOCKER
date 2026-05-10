#!/bin/bash
# Script de instalación para Instancia 1 - Servidor Maestro

echo "=== Instalación de Servidor Maestro (Instancia 1) ==="

echo "Instalando MariaDB..."
sudo dnf update -y
sudo dnf install mariadb105-server -y

echo "Iniciando y habilitando MariaDB..."
sudo systemctl start mariadb
sudo systemctl enable mariadb

echo "Instalando Python y dependencias..."
sudo dnf install python3-pip -y
pip3 install -r requirements.txt

echo "Configurando MariaDB para conexiones remotas..."
# Copiar configuración (requiere intervención manual)
echo "Debe editar /etc/my.cnf.d/mariadb-server.cnf y establecer bind-address = 0.0.0.0"

echo "Ejecutando configuración segura de MySQL..."
sudo mysql_secure_installation

echo "Creando base de datos y usuario con nueva estructura..."
mysql -u root -p < setup_database.sql

echo "Iniciando servidor API con estructura de datos actualizada..."
python3 server_api.py > api.log 2>&1 &

echo "Instalación completada. Verifique que la API esté corriendo en el puerto 5000"
