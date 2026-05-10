-- Crear base de datos y tablas para el sistema de farmacias
CREATE DATABASE farmacias_db;
USE farmacias_db;

CREATE TABLE farmacias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    local_id VARCHAR(50),
    local_nombre VARCHAR(255),
    comuna_nombre VARCHAR(100),
    localidad_nombre VARCHAR(100),
    local_direccion VARCHAR(255),
    funcionamiento_hora_apertura TIME,
    funcionamiento_hora_cierre TIME,
    funcionamiento_dia VARCHAR(20),  -- lunes, martes...
    fk_region VARCHAR(10),
    fk_comuna VARCHAR(10),
    local_telefono VARCHAR(50)
);

-- Crear usuario para las otras instancias
CREATE USER 'api_user'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON farmacias_db.* TO 'api_user'@'%';
FLUSH PRIVILEGES;
