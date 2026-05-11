#!/bin/bash

# Script para descargar y ejecutar desde Docker Hub
# Uso: ./usar_desde_dockerhub.sh [servidor|cliente]

SERVICIO=${1:-servidor}
DOCKERHUB_USER="sebamugi"
SERVER_IMAGE="farmacias-server"
CLIENT_IMAGE="farmacias-client"

echo "=== Descargando desde Docker Hub ==="

case $SERVICIO in
    "servidor"|"server")
        echo "Iniciando servidor (Instancia 1)..."
        echo "Descargando imagen: $DOCKERHUB_USER/$SERVER_IMAGE:latest"
        docker pull $DOCKERHUB_USER/$SERVER_IMAGE:latest
        
        echo "Iniciando contenedor en puerto 5000..."
        docker run -d --name farmacias-server \
            -p 5000:5000 \
            -e DB_HOST=localhost \
            -e DB_USER=api_user \
            -e DB_PASSWORD=tu_password_seguro \
            -e DB_DATABASE=farmacias_db \
            $DOCKERHUB_USER/$SERVER_IMAGE:latest
            
        echo "Servidor iniciado en: http://localhost:5000"
        echo "Para ver logs: docker logs farmacias-server"
        echo "Para detener: docker stop farmacias-server"
        ;;
        
    "cliente"|"client")
        echo "Iniciando cliente (Instancia 2)..."
        echo "Descargando imagen: $DOCKERHUB_USER/$CLIENT_IMAGE:latest"
        docker pull $DOCKERHUB_USER/$CLIENT_IMAGE:latest
        
        echo "Iniciando contenedor en puerto 80..."
        docker run -d --name farmacias-client \
            -p 80:80 \
            -e URL_MAESTRA=http://localhost:5000/farmacias \
            $DOCKERHUB_USER/$CLIENT_IMAGE:latest
            
        echo "Cliente iniciado en: http://localhost"
        echo "Para ver logs: docker logs farmacias-client"
        echo "Para detener: docker stop farmacias-client"
        ;;
        
    "ambos"|"both")
        echo "Iniciando ambos servicios..."
        
        # Iniciar servidor
        echo "Descargando imagen del servidor..."
        docker pull $DOCKERHUB_USER/$SERVER_IMAGE:latest
        docker run -d --name farmacias-server \
            -p 5000:5000 \
            -e DB_HOST=localhost \
            -e DB_USER=api_user \
            -e DB_PASSWORD=tu_password_seguro \
            -e DB_DATABASE=farmacias_db \
            $DOCKERHUB_USER/$SERVER_IMAGE:latest
            
        # Esperar a que el servidor inicie
        echo "Esperando 10 segundos para que el servidor inicie..."
        sleep 10
        
        # Iniciar cliente
        echo "Descargando imagen del cliente..."
        docker pull $DOCKERHUB_USER/$CLIENT_IMAGE:latest
        docker run -d --name farmacias-client \
            -p 80:80 \
            -e URL_MAESTRA=http://host.docker.internal:5000/farmacias \
            $DOCKERHUB_USER/$CLIENT_IMAGE:latest
            
        echo "Ambos servicios iniciados:"
        echo "Servidor: http://localhost:5000"
        echo "Cliente: http://localhost"
        ;;
        
    "detener"|"stop")
        echo "Deteniendo todos los contenedores..."
        docker stop farmacias-server 2>/dev/null || echo "Servidor no estaba corriendo"
        docker stop farmacias-client 2>/dev/null || echo "Cliente no estaba corriendo"
        docker rm farmacias-server 2>/dev/null || echo "Contenedor servidor no existe"
        docker rm farmacias-client 2>/dev/null || echo "Contenedor cliente no existe"
        echo "Servicios detenidos"
        ;;
        
    *)
        echo "Uso: $0 [servidor|cliente|ambos|detener]"
        echo ""
        echo "Opciones:"
        echo "  servidor  - Inicia solo el servidor (Instancia 1)"
        echo "  cliente   - Inicia solo el cliente (Instancia 2)"
        echo "  ambos     - Inicia ambos servicios"
        echo "  detener   - Detiene todos los servicios"
        echo ""
        echo "Ejemplos:"
        echo "  $0 servidor"
        echo "  $0 cliente"
        echo "  $0 ambos"
        echo "  $0 detener"
        exit 1
        ;;
esac

echo ""
echo "=== Operación completada ==="
