<?php
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

$servidor = "localhost";
$usuario = "admin_clima"; // Corregido nombre de variable
$password = "kevin2090";
$base_datos = "farmacias_db"; // Corregido nombre de variable

$conexion = new mysqli($servidor, $usuario, $password, $base_datos);

if ($conexion->connect_error) {
    die(json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]));
}

// OBTENER EL MÉTODO (GET o POST)
$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo == 'POST') {
    // --- LÓGICA PARA REGISTRAR (INSERT) ---
    $json = file_get_contents('php://input');
    $datos = json_decode($json, true);

    if (isset($datos['local_nombre'])) {
        $stmt = $conexion->prepare("INSERT INTO turnos (local_nombre, comuna_nombre, local_direccion, local_telefono, funcionamiento_dia, funcionamiento_hora_apertura, funcionamiento_hora_cierre) VALUES (?, ?, ?, ?, ?, ?)");
        
        $stmt->bind_param("sssssss", 
            $datos['local_nombre'], 
            $datos['comuna_nombre'], 
            $datos['local_direccion'], 
            $datos['local_telefono'], 
            $datos['funcionamiento_dia'], 
            $datos['funcionamiento_hora_apertura'], 
            $datos['funcionamiento_hora_cierre']
        );

        if ($stmt->execute()) {
            http_response_code(201);
            echo json_encode(["message" => "Farmacia registrada con éxito"]);
        } else {
            http_response_code(500);
            echo json_encode(["error" => "Error al insertar: " . $stmt->error]);
        }
        $stmt->close();
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Datos incompletos"]);
    }

} elseif (isset($_GET['comunas']) && $_GET['comunas'] == 'true') {
    // --- LÓGICA PARA OBTENER COMUNAS ÚNICAS ---
    $sql = "SELECT DISTINCT comuna_nombre FROM turnos ORDER BY comuna_nombre";
    $resultado = $conexion->query($sql);
    $comunas = array();

    if ($resultado && $resultado->num_rows > 0) {
        while ($fila = $resultado->fetch_assoc()) {
            $comunas[] = $fila['comuna_nombre'];
        }
    }
    echo json_encode($comunas, JSON_UNESCAPED_UNICODE);

} else {
    // --- LÓGICA PARA CONSULTAR (GET) ---
    $sql = "SELECT * FROM turnos";
    
    // Si envías una comuna por parámetro GET en la URL
    if (isset($_GET['comuna']) && !empty($_GET['comuna'])) {
        $comuna = $conexion->real_escape_string($_GET['comuna']);
        $sql .= " WHERE comuna_nombre = '$comuna'";
    }

    // Filtro para farmacias abiertas
    if (isset($_GET['abiertas']) && $_GET['abiertas'] == 'true') {
        $dia_semana_map = ['domingo', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado'];
        $dia_actual = $dia_semana_map[date('w')];
        $hora_actual = date('H:i:s');
        
        if (isset($_GET['comuna']) && !empty($_GET['comuna'])) {
            $sql .= " AND funcionamiento_dia = '$dia_actual' AND '$hora_actual' BETWEEN funcionamiento_hora_apertura AND funcionamiento_hora_cierre";
        } else {
            $sql .= " WHERE funcionamiento_dia = '$dia_actual' AND '$hora_actual' BETWEEN funcionamiento_hora_apertura AND funcionamiento_hora_cierre";
        }
    }

    $resultado = $conexion->query($sql);
    $farmacias = array();

    if ($resultado && $resultado->num_rows > 0) {
        while ($fila = $resultado->fetch_assoc()) {
            $farmacias[] = $fila;
        }
    }
    echo json_encode($farmacias, JSON_UNESCAPED_UNICODE);
}

$conexion->close();
?>