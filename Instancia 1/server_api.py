from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import mysql.connector
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'farmacias_secret_key_2024'

# Configuración de conexión
db_config = {
    'host': 'localhost',
    'user': 'api_user',
    'password': 'tu_password_seguro',
    'database': 'farmacias_db'
}

def query_db(query, args=(), one=False):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def validar_farmacia(datos):
    errores = []
    
    # Validar local_nombre
    if not datos.get('local_nombre', '').strip():
        errores.append('El nombre de la farmacia es requerido')
    elif len(datos['local_nombre']) > 255:
        errores.append('El nombre no puede exceder 255 caracteres')
    
    # Validar comuna_nombre
    if not datos.get('comuna_nombre', '').strip():
        errores.append('La comuna es requerida')
    elif len(datos['comuna_nombre']) > 100:
        errores.append('La comuna no puede exceder 100 caracteres')
    
    # Validar local_direccion
    if not datos.get('local_direccion', '').strip():
        errores.append('La dirección es requerida')
    elif len(datos['local_direccion']) > 255:
        errores.append('La dirección no puede exceder 255 caracteres')
    
    # Validar local_telefono
    telefono = datos.get('local_telefono', '').strip()
    if not telefono:
        errores.append('El teléfono es requerido')
    elif len(telefono) > 50:
        errores.append('El teléfono no puede exceder 50 caracteres')
    elif not re.match(r'^[\d\+\-\s\(\)]+$', telefono):
        errores.append('El teléfono solo puede contener números, +, -, () y espacios')
    
    # Validar funcionamiento_dia
    dias_validos = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    dia_semana = datos.get('funcionamiento_dia', '').strip().lower()
    if not dia_semana:
        errores.append('El día de semana es requerido')
    elif dia_semana not in dias_validos:
        errores.append('Día de semana inválido. Debe ser: ' + ', '.join(dias_validos))
    
    # Validar horas
    try:
        apertura = datos.get('funcionamiento_hora_apertura', '').strip()
        cierre = datos.get('funcionamiento_hora_cierre', '').strip()
        
        if not apertura:
            errores.append('La hora de apertura es requerida')
        else:
            datetime.strptime(apertura, '%H:%M:%S')
            
        if not cierre:
            errores.append('La hora de cierre es requerida')
        else:
            datetime.strptime(cierre, '%H:%M:%S')
            
        if apertura and cierre and apertura >= cierre:
            errores.append('La hora de apertura debe ser anterior a la hora de cierre')
            
    except ValueError:
        errores.append('Formato de hora inválido. Use HH:MM:SS')
    
    return errores

def esta_abierta(farmacia):
    """Verifica si una farmacia está abierta en este momento"""
    ahora = datetime.now()
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual = dias[ahora.weekday()]
    hora_actual = ahora.strftime('%H:%M:%S')
    
    return (farmacia['funcionamiento_dia'].lower() == dia_actual and 
            farmacia['funcionamiento_hora_apertura'] <= hora_actual <= farmacia['funcionamiento_hora_cierre'])

def agregar_estado_farmacias(farmacias):
    """Agrega el estado actual a cada farmacia"""
    for farmacia in farmacias:
        farmacia['esta_abierta'] = esta_abierta(farmacia)
        farmacia['estado_actual'] = 'Abierta' if farmacia['esta_abierta'] else 'Cerrada'
        farmacia['hora_actual'] = datetime.now().strftime('%H:%M:%S')
        farmacia['dia_actual'] = datetime.now().strftime('%A')
    return farmacias

# API Endpoints
@app.route('/farmacias', methods=['GET'])
def get_farmacias():
    comuna = request.args.get('comuna')
    solo_abiertas = request.args.get('abiertas')  # True/False
    
    sql = "SELECT * FROM farmacias WHERE comuna_nombre = %s"
    params = [comuna]
    
    if solo_abiertas == 'true':
        ahora = datetime.now()
        # Mapeo de días al español según el dataset
        dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        dia_nombre = dias[ahora.weekday()]
        hora_actual = ahora.strftime('%H:%M:%S')
        
        sql += " AND funcionamiento_dia = %s AND %s BETWEEN funcionamiento_hora_apertura AND funcionamiento_hora_cierre"
        params.extend([dia_nombre, hora_actual])
    
    results = query_db(sql, params)
    # Agregar estado actual a cada farmacia
    results = agregar_estado_farmacias(results)
    return jsonify(results)

@app.route('/farmacias', methods=['POST'])
def add_farmacia():
    datos = request.json
    
    # Validar datos
    errores = validar_farmacia(datos)
    if errores:
        return jsonify({"status": "error", "message": "Datos inválidos", "errors": errores}), 400
    
    sql = """INSERT INTO farmacias (local_nombre, comuna_nombre, local_direccion, local_telefono, funcionamiento_dia, funcionamiento_hora_apertura, funcionamiento_hora_cierre)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    valores = (datos['local_nombre'], datos['comuna_nombre'], datos['local_direccion'],
               datos['local_telefono'], datos['funcionamiento_dia'], datos['funcionamiento_hora_apertura'], datos['funcionamiento_hora_cierre'])
    
    query_db(sql, valores)
    return jsonify({"status": "success", "message": "Farmacia registrada"}), 201

@app.route('/farmacias/<int:id>', methods=['GET'])
def get_farmacia(id):
    farmacia = query_db("SELECT * FROM farmacias WHERE id = %s", [id], one=True)
    if not farmacia:
        return jsonify({"status": "error", "message": "Farmacia no encontrada"}), 404
    return jsonify(farmacia)

@app.route('/farmacias/<int:id>', methods=['PUT'])
def update_farmacia(id):
    datos = request.json
    
    # Validar datos
    errores = validar_farmacia(datos)
    if errores:
        return jsonify({"status": "error", "message": "Datos inválidos", "errors": errores}), 400
    
    # Verificar que existe
    farmacia = query_db("SELECT id FROM farmacias WHERE id = %s", [id], one=True)
    if not farmacia:
        return jsonify({"status": "error", "message": "Farmacia no encontrada"}), 404
    
    sql = """UPDATE farmacias SET local_nombre = %s, comuna_nombre = %s, local_direccion = %s, 
             local_telefono = %s, funcionamiento_dia = %s, funcionamiento_hora_apertura = %s, funcionamiento_hora_cierre = %s 
             WHERE id = %s"""
    valores = (datos['local_nombre'], datos['comuna_nombre'], datos['local_direccion'],
               datos['local_telefono'], datos['funcionamiento_dia'], datos['funcionamiento_hora_apertura'], datos['funcionamiento_hora_cierre'], id)
    
    query_db(sql, valores)
    return jsonify({"status": "success", "message": "Farmacia actualizada"})

@app.route('/farmacias/<int:id>', methods=['DELETE'])
def delete_farmacia(id):
    # Verificar que existe
    farmacia = query_db("SELECT id FROM farmacias WHERE id = %s", [id], one=True)
    if not farmacia:
        return jsonify({"status": "error", "message": "Farmacia no encontrada"}), 404
    
    query_db("DELETE FROM farmacias WHERE id = %s", [id])
    return jsonify({"status": "success", "message": "Farmacia eliminada"})

@app.route('/farmacias/comunas', methods=['GET'])
def get_comunas():
    comunas = query_db("SELECT DISTINCT comuna_nombre FROM farmacias ORDER BY comuna_nombre")
    return jsonify([c['comuna_nombre'] for c in comunas])

@app.route('/farmacias/abiertas', methods=['GET'])
def get_farmacias_abiertas():
    """Endpoint específico para farmacias abiertas ahora"""
    ahora = datetime.now()
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual = dias[ahora.weekday()]
    hora_actual = ahora.strftime('%H:%M:%S')
    
    sql = """
        SELECT * FROM farmacias 
        WHERE funcionamiento_dia = %s 
        AND %s BETWEEN funcionamiento_hora_apertura AND funcionamiento_hora_cierre
    """
    params = [dia_actual, hora_actual]
    
    results = query_db(sql, params)
    # Agregar estado actual a cada farmacia
    results = agregar_estado_farmacias(results)
    
    return jsonify({
        "farmacias_abiertas": results,
        "total_abiertas": len(results),
        "hora_actual": hora_actual,
        "dia_actual": dia_actual,
        "timestamp": ahora.isoformat()
    })

@app.route('/farmacias/estadisticas', methods=['GET'])
def get_estadisticas():
    total = query_db("SELECT COUNT(*) as total FROM farmacias", one=True)
    por_comuna = query_db("""
        SELECT comuna_nombre, COUNT(*) as cantidad 
        FROM farmacias 
        GROUP BY comuna_nombre 
        ORDER BY cantidad DESC
    """)
    por_dia = query_db("""
        SELECT funcionamiento_dia, COUNT(*) as cantidad 
        FROM farmacias 
        GROUP BY funcionamiento_dia 
        ORDER BY cantidad DESC
    """)
    
    # Calcular farmacias abiertas ahora
    todas_farmacias = query_db("SELECT * FROM farmacias")
    farmacias_con_estado = agregar_estado_farmacias(todas_farmacias)
    abiertas_ahora = [f for f in farmacias_con_estado if f['esta_abierta']]
    
    return jsonify({
        "total_farmacias": total['total'],
        "abiertas_ahora": len(abiertas_ahora),
        "cerradas_ahora": total['total'] - len(abiertas_ahora),
        "por_comuna": por_comuna,
        "por_dia": por_dia,
        "hora_actual": datetime.now().strftime('%H:%M:%S'),
        "dia_actual": datetime.now().strftime('%A')
    })

# Interfaz Web - Servidor Maestro
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/farmacias_web')
def farmacias_web():
    comuna = request.args.get('comuna', '')
    search_query = request.args.get('search', '')
    
    sql = "SELECT * FROM farmacias"
    params = []
    conditions = []
    
    if comuna:
        conditions.append("comuna_nombre = %s")
        params.append(comuna)
    
    if search_query:
        conditions.append("(local_nombre LIKE %s OR local_direccion LIKE %s)")
        params.extend([f'%{search_query}%', f'%{search_query}%'])
    
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    
    sql += " ORDER BY local_nombre"
    
    farmacias = query_db(sql, params) if params else query_db(sql)
    comunas = query_db("SELECT DISTINCT comuna FROM farmacias ORDER BY comuna")
    
    return render_template('farmacias.html', 
                         farmacias=farmacias, 
                         comunas=[c['comuna_nombre'] for c in comunas],
                         comuna_selected=comuna,
                         search_query=search_query)

@app.route('/farmacias_web/new')
def new_farmacia():
    return render_template('farmacia_form.html', farmacia=None, action='create')

@app.route('/farmacias_web/edit/<int:id>')
def edit_farmacia(id):
    farmacia = query_db("SELECT * FROM farmacias WHERE id = %s", [id], one=True)
    if not farmacia:
        flash('Farmacia no encontrada', 'error')
        return redirect(url_for('farmacias_web'))
    return render_template('farmacia_form.html', farmacia=farmacia, action='edit')

@app.route('/farmacias_web/create', methods=['POST'])
def create_farmacia_web():
    datos = {
        'nombre': request.form['nombre'],
        'comuna': request.form['comuna'],
        'direccion': request.form['direccion'],
        'telefono': request.form['telefono'],
        'dia_semana': request.form['dia_semana'],
        'apertura': request.form['apertura'],
        'cierre': request.form['cierre']
    }
    
    errores = validar_farmacia(datos)
    if errores:
        for error in errores:
            flash(error, 'error')
        return render_template('farmacia_form.html', farmacia=datos, action='create')
    
    sql = """INSERT INTO farmacias (nombre, comuna, direccion, telefono, dia_semana, apertura, cierre)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    valores = (datos['nombre'], datos['comuna'], datos['direccion'],
               datos['telefono'], datos['dia_semana'], datos['apertura'], datos['cierre'])
    
    query_db(sql, valores)
    flash('Farmacia registrada exitosamente', 'success')
    return redirect(url_for('farmacias_web'))

@app.route('/farmacias_web/update/<int:id>', methods=['POST'])
def update_farmacia_web(id):
    datos = {
        'nombre': request.form['nombre'],
        'comuna': request.form['comuna'],
        'direccion': request.form['direccion'],
        'telefono': request.form['telefono'],
        'dia_semana': request.form['dia_semana'],
        'apertura': request.form['apertura'],
        'cierre': request.form['cierre']
    }
    
    errores = validar_farmacia(datos)
    if errores:
        for error in errores:
            flash(error, 'error')
        farmacia = query_db("SELECT * FROM farmacias WHERE id = %s", [id], one=True)
        return render_template('farmacia_form.html', farmacia=datos, action='edit', id=id)
    
    sql = """UPDATE farmacias SET nombre = %s, comuna = %s, direccion = %s, 
             telefono = %s, dia_semana = %s, apertura = %s, cierre = %s 
             WHERE id = %s"""
    valores = (datos['nombre'], datos['comuna'], datos['direccion'],
               datos['telefono'], datos['dia_semana'], datos['apertura'], datos['cierre'], id)
    
    query_db(sql, valores)
    flash('Farmacia actualizada exitosamente', 'success')
    return redirect(url_for('farmacias_web'))

@app.route('/farmacias_web/delete/<int:id>')
def delete_farmacia_web(id):
    farmacia = query_db("SELECT id FROM farmacias WHERE id = %s", [id], one=True)
    if not farmacia:
        flash('Farmacia no encontrada', 'error')
        return redirect(url_for('farmacias_web'))
    
    query_db("DELETE FROM farmacias WHERE id = %s", [id])
    flash('Farmacia eliminada exitosamente', 'success')
    return redirect(url_for('farmacias_web'))

@app.route('/estadisticas')
def estadisticas_web():
    total = query_db("SELECT COUNT(*) as total FROM farmacias", one=True)
    por_comuna = query_db("""
        SELECT comuna_nombre, COUNT(*) as cantidad 
        FROM farmacias 
        GROUP BY comuna_nombre 
        ORDER BY cantidad DESC
        LIMIT 10
    """)
    por_dia = query_db("""
        SELECT funcionamiento_dia, COUNT(*) as cantidad 
        FROM farmacias 
        GROUP BY funcionamiento_dia 
        ORDER BY cantidad DESC
    """)
    
    return render_template('estadisticas.html', 
                         total_farmacias=total['total'],
                         por_comuna=por_comuna,
                         por_dia=por_dia)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
