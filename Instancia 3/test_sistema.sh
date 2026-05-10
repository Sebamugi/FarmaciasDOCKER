#!/bin/bash
# Script para pruebas del sistema completo

echo "=== Test 1: Registro desde Instancia 3 ==="
echo "Registrando una farmacia de prueba..."
curl -X POST http://localhost/registrar \
-H "Content-Type: application/json" \
-d '{
    "nombre": "Farmacia Universitaria",
    "comuna": "Concepcion",
    "direccion": "Barrio Universitario s/n",
    "telefono": "+5641222222",
    "dia_semana": "martes",
    "apertura": "08:00:00",
    "cierre": "21:00:00"
}'

echo -e "\n\n=== Test 2: Consulta desde Instancia 2 ==="
echo "Consultando farmacias en Concepción..."
echo "Ejecutar desde Instancia 2 o navegador:"
echo "curl 'http://IP_INSTANCIA_2/consultar?comuna=Concepcion'"

echo -e "\n\n=== Verificación final ==="
echo "Verificar que la farmacia registrada aparezca en la consulta"
