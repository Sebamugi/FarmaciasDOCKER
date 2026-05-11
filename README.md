# FarmaciasDOCKER - Sistema Distribuido de Farmacias

Sistema completo de gestión de farmacias con arquitectura distribuida en AWS Cloud Computing, implementado con Flask, Docker y MariaDB.

## 🏗️ Arquitectura

### Instancia 1 - Servidor Maestro (API PHP)
- **Base de Datos**: MariaDB con estructura de datos real del gobierno
- **API RESTful**: Endpoints completos para CRUD de farmacias
- **Endpoint Principal**: `http://32.197.236.185/Farmacias_api.php`
- **Validaciones**: Verificación de horarios en tiempo real

### Instancia 2 - Cliente Flask (Portal Web)
- **Portal Público**: Interfaz de búsqueda y registro
- **Consumo API**: Conexión con servidor maestro
- **Validación Local**: Validación básica de datos
- **Docker**: Contenedor completo para producción

## 🚀 Características Principales

### ✅ Funcionalidades Completas
- **Búsqueda Avanzada**: Por comuna, nombre, dirección
- **Registro de Farmacias**: Formulario completo con validaciones
- **Verificación de Horarios**: Estado en tiempo real basado en hora del sistema
- **Estadísticas Interactivas**: Contador de farmacias abiertas/cerradas
- **Filtros Dinámicos**: Comunas y búsqueda textual

### 🎨 Interfaz Moderna
- **Bootstrap 5**: Diseño responsivo y moderno
- **Font Awesome**: Iconos profesionales
- **Actualización Automática**: Estados actualizados dinámicamente
- **Indicadores Visuales**: Badges de estado (abierta/cerrada)

### 🔧 Características Técnicas
- **Estructura Real**: Datos compatibles con formato gubernamental
- **Validaciones**: Servidor y cliente
- **Seguridad**: Sanitización de datos y protección XSS
- **Docker**: Contenerización completa
- **Logging Detallado**: Para depuración y monitoreo

## 📊 Estructura de Datos

### Tabla: turnos
```sql
CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    local_id VARCHAR(50),
    local_nombre VARCHAR(255),
    comuna_nombre VARCHAR(100),
    localidad_nombre VARCHAR(100),
    local_direccion VARCHAR(255),
    funcionamiento_hora_apertura TIME,
    funcionamiento_hora_cierre TIME,
    funcionamiento_dia VARCHAR(20),
    fk_region VARCHAR(10),
    fk_comuna VARCHAR(10),
    local_telefono VARCHAR(50)
);
```

### Estructura JSON
```json
{
    "id": "34",
    "fecha": "2026-05-07",
    "local_id": "2270",
    "local_nombre": "LA ESTRELLA",
    "comuna_nombre": "ARAUCO",
    "localidad_nombre": "ARAUCO",
    "local_direccion": "CONDELL 654",
    "funcionamiento_hora_apertura": "09:00:00",
    "funcionamiento_hora_cierre": "08:59:00",
    "funcionamiento_dia": "jueves",
    "fk_region": "10",
    "fk_comuna": "200",
    "local_telefono": "+56412551009"
}
```

## 🛠️ Instalación y Despliegue

### Requisitos
- Python 3.9+
- Docker y Docker Hub
- AWS EC2
- MariaDB

### Instancia 1 - Servidor Maestro (API PHP)

```bash
# Clonar repositorio
git clone https://github.com/Sebamugi/FarmaciasDOCKER.git
cd FarmaciasDocker/Instancia\ 1

# Configurar base de datos
mysql -u root -p < setup_database.sql

# Configurar Apache (si aplica)
# Copiar farmacia_api.php a /var/www/html/
```

### Instancia 2 - Cliente Flask (Docker)

```bash
# Construir imagen Docker
cd Instancia\ 2
docker build -t farmacias-client:latest .

# Ejecutar contenedor
docker run -d --name app_cliente -p 80:80 farmacias-client:latest

# O usar desde Docker Hub
docker run -d --name app_cliente -p 80:80 sebamugi/farmacias-client:latest
```

## 📡 API Endpoints

### Endpoints Principales
- `GET /Farmacias_api.php` - Listar farmacias
- `POST /Farmacias_api.php` - Crear farmacia
- `GET /Farmacias_api.php?comunas=true` - Listar comunas únicas

### Parámetros de Búsqueda
- `?comuna=nombre` - Filtrar por comuna
- `?abiertas=true` - Solo farmacias abiertas
- `?search=texto` - Búsqueda por nombre/dirección

## 🌐 Interfaces Web

### Instancia 2 - Cliente Flask
- **Portal Principal**: `http://localhost/`
- **Búsqueda**: `http://localhost/buscar`
- **Registro**: `http://localhost/registrar_form`
- **Estadísticas**: `http://localhost/estadisticas`

## ⏰ Verificación de Horarios

El sistema verifica automáticamente si las farmacias están abiertas basándose en:

1. **Hora del Sistema**: Usa `datetime.now()` con timezone Chile
2. **Día de Semana**: Mapeo a español
3. **Horario Configurado**: Rango apertura-cierre
4. **Actualización Automática**: En cada consulta

### Lógica de Verificación
```python
def esta_abierta(farmacia):
    ahora = datetime.now(pytz.timezone('America/Santiago'))
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual = dias[ahora.weekday()]
    hora_actual = ahora.strftime('%H:%M')
    
    return (farmacia['funcionamiento_dia'].lower() == dia_actual and 
            farmacia['funcionamiento_hora_apertura'] <= hora_actual <= farmacia['funcionamiento_hora_cierre'])
```

## 🔧 Configuración

### Variables de Entorno (Instancia 2)
```python
# En app.py
URL_MAESTRA = "http://32.197.236.185/Farmacias_api.php"
SECRET_KEY = '1231234'
```

### Base de Datos (Instancia 1)
```sql
CREATE DATABASE farmacias_db;
CREATE USER 'api_user'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON farmacias_db.* TO 'api_user'@'%';
```

## 📱 Tecnologías Utilizadas

- **Backend**: PHP 8.0 (Instancia 1), Python 3.9 + Flask (Instancia 2)
- **Base de Datos**: MariaDB 10.5
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Contenerización**: Docker
- **Nube**: AWS EC2, Docker Hub
- **Comunicación**: HTTP/HTTPS, REST API

## 🚀 Despliegue en AWS

### Configuración de Instancias
1. **Instancia 1**: EC2 con API PHP y MariaDB
2. **Instancia 2**: EC2 con contenedor Docker del cliente Flask

### Seguridad
- Configurar Security Groups
- Usar SSH keys
- Configurar firewall
- Actualizar sistemas

## 📊 Monitoreo y Logs

### Logs del Sistema
- **API PHP**: Logs de Apache/PHP
- **Cliente Flask**: Logging detallado implementado
- **Docker**: `docker logs app_cliente`

### Estadísticas en Tiempo Real
- Farmacias abiertas/cerradas
- Total por comuna
- Hora actual del sistema (Chile)




**Desarrollado por**: Sebamugi  
**Última actualización**: Mayo 2026  
**Estado**: ✅ Producción Ready  
**Repositorio**: https://github.com/Sebamugi/FarmaciasDOCKER.git
