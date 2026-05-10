FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer puerto 5000
EXPOSE 5000

# Variable de entorno para la configuración de la base de datos
ENV DB_HOST=localhost
ENV DB_USER=api_user
ENV DB_PASSWORD=tu_password_seguro
ENV DB_DATABASE=farmacias_db

CMD ["python", "server_api.py"]
