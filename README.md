# FarmaciasDOCKER - Sistema Distribuido de Farmacias

Sistema completo de gestión de farmacias con arquitectura distribuida en AWS Cloud Computing, implementado con Flask, Docker y MariaDB.

## 🏗️ Arquitectura

### Instancia 1 - Servidor Maestro
- **Base de Datos**: MariaDB con estructura de datos real del gobierno
- **API RESTful**: Endpoints completos para CRUD de farmacias
- **Interfaz Web**: Dashboard con gestión visual completa
- **Validaciones**: Verificación de horarios en tiempo real

### Instancia 2 - Cliente Docker
- **Portal Público**: Interfaz de búsqueda y registro
- **Consumo API**: Conexión con servidor maestro
- **Validación Local**: Validación básica de datos

### Instancia 3 - Réplica Automática
- **Despliegue**: Scripts automatizados
- **Docker Hub**: Imágenes preconfiguradas

## 🚀 Características Principales

### ✅ Funcionalidades Completas
- **CRUD Visual**: Crear, leer, actualizar, eliminar farmacias
- **Búsqueda Avanzada**: Por comuna, nombre, dirección
- **Verificación de Horarios**: Estado en tiempo real basado en hora del sistema
- **Estadísticas Interactivas**: Gráficos con Chart.js
- **Exportación de Datos**: CSV y reportes

### 🎨 Interfaz Moderna
- **Bootstrap 5**: Diseño responsivo y moderno
- **Font Awesome**: Iconos profesionales
- **Actualización Automática**: Estados actualizados cada 30 segundos
- **Indicadores Visuales**: Badges de estado (abierta/cerrada)

### 🔧 Características Técnicas
- **Estructura Real**: Datos compatibles con formato gubernamental
- **Validaciones**: Servidor y cliente
- **Seguridad**: Sanitización de datos y protección XSS
- **Docker**: Contenerización completa

## 📊 Estructura de Datos

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
- Docker y Docker Compose
- AWS EC2 (3 instancias)
- MariaDB

### Instancia 1 - Servidor Maestro

```bash
# Clonar repositorio
git clone https://github.com/Sebamugi/FarmaciasDOCKER.git
cd FarmaciasDocker/Instancia\ 1

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
mysql -u root -p < setup_database.sql

# Iniciar servidor
python server_api.py
```

### Docker Compose (Recomendado)

```bash
# En Instancia 1
cd Instancia\ 1
docker-compose up -d

# En Instancia 2
cd Instancia\ 2
docker-compose up -d
```

### Instancia 2 - Cliente

```bash
cd Instancia\ 2
pip install -r requirements.txt
python app.py
```

### Instancia 3 - Despliegue Automático

```bash
cd Instancia\ 3
chmod +x *.sh
./despliegue_dockerhub.sh
```

## 📡 API Endpoints

### Endpoints Principales
- `GET /farmacias` - Listar farmacias
- `POST /farmacias` - Crear farmacia
- `GET /farmacias/{id}` - Obtener farmacia
- `PUT /farmacias/{id}` - Actualizar farmacia
- `DELETE /farmacias/{id}` - Eliminar farmacia

### Endpoints Especiales
- `GET /farmacias/comunas` - Listar comunas
- `GET /farmacias/estadisticas` - Estadísticas completas
- `GET /farmacias/abiertas` - Farmacias abiertas ahora

### Parámetros de Búsqueda
- `?comuna=nombre` - Filtrar por comuna
- `?abiertas=true` - Solo farmacias abiertas
- `?search=texto` - Búsqueda por nombre/dirección

## 🌐 Interfaces Web

### Instancia 1 - Servidor Maestro
- **Dashboard**: `http://localhost:5000/`
- **Gestión**: `http://localhost:5000/farmacias_web`
- **Estadísticas**: `http://localhost:5000/estadisticas`

### Instancia 2 - Cliente
- **Portal**: `http://localhost/`
- **Búsqueda**: `http://localhost/buscar`
- **Registro**: `http://localhost/registrar_form`

## ⏰ Verificación de Horarios

El sistema verifica automáticamente si las farmacias están abiertas basándose en:

1. **Hora del Sistema**: Usa `datetime.now()`
2. **Día de Semana**: Mapeo a español
3. **Horario Configurado**: Rango apertura-cierre
4. **Actualización Automática**: Cada 30 segundos

### Lógica de Verificación
```python
def esta_abierta(farmacia):
    ahora = datetime.now()
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual = dias[ahora.weekday()]
    hora_actual = ahora.strftime('%H:%M:%S')
    
    return (farmacia['funcionamiento_dia'].lower() == dia_actual and 
            farmacia['funcionamiento_hora_apertura'] <= hora_actual <= farmacia['funcionamiento_hora_cierre'])
```

## 🔧 Configuración

### Variables de Entorno
```bash
DB_HOST=localhost
DB_USER=api_user
DB_PASSWORD=tu_password_seguro
DB_DATABASE=farmacias_db
URL_MAESTRA=http://172.31.xx.xx:5000/farmacias
```

### Base de Datos
```sql
CREATE DATABASE farmacias_db;
CREATE USER 'api_user'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON farmacias_db.* TO 'api_user'@'%';
```

## 📱 Tecnologías Utilizadas

- **Backend**: Python 3.9, Flask
- **Base de Datos**: MariaDB 10.5
- **Frontend**: Bootstrap 5, Font Awesome 6, Chart.js
- **Contenerización**: Docker, Docker Compose
- **Nube**: AWS EC2, Docker Hub
- **Comunicación**: HTTP/HTTPS, REST API

## 🚀 Despliegue en AWS

### Configuración de Instancias
1. **Instancia 1**: t2.micro (Servidor Maestro)
2. **Instancia 2**: t2.micro (Cliente)
3. **Instancia 3**: t2.micro (Réplica)

### Seguridad
- Configurar Security Groups
- Usar SSH keys
- Configurar firewall
- Actualizar sistemas

## 📊 Monitoreo y Logs

### Logs del Sistema
- **Servidor API**: `api.log`
- **Cliente**: `client.log`
- **Docker**: `docker logs`

### Estadísticas en Tiempo Real
- Farmacias abiertas/cerradas
- Total por comuna
- Distribución por día
- Hora actual del sistema

## 🤝 Contribuciones

1. Fork del repositorio
2. Crear feature branch
3. Realizar cambios
4. Hacer commit
5. Push al branch
6. Crear Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

## 📞 Soporte

- **Issues**: GitHub Issues
- **Documentación**: Wiki del proyecto
- **Email**: soporte@farmacias.cl

## 🔄 Versiones

- **v1.0**: Sistema básico con API
- **v2.0**: Interfaz web completa
- **v2.1**: Estructura de datos real
- **v2.2**: Verificación de horarios en tiempo real

---

**Desarrollado por**: Sebamugi  
**Última actualización**: Mayo 2024  
**Estado**: ✅ Producción Ready
