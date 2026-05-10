from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'farmacias_client_secret_2024'

# REEMPLAZA CON LA IP PRIVADA O PÚBLICA DE LA INSTANCIA 1
URL_MAESTRA = "http://172.31.xx.xx:5000/farmacias"

# API Endpoints
@app.route('/consultar', methods=['GET'])
def consultar():
    comuna = request.args.get('comuna')
    abiertas = request.args.get('abiertas', 'false')
    
    # Redirige la consulta a la Instancia 1
    response = requests.get(URL_MAESTRA, params={'comuna': comuna, 'abiertas': abiertas})
    
    return jsonify(response.json()), response.status_code

@app.route('/registrar', methods=['POST'])
def registrar():
    # Recibe datos del cliente y los manda a la Instancia 1
    datos = request.json
    response = requests.post(URL_MAESTRA, json=datos)
    
    return jsonify(response.json()), response.status_code

# Interfaz Web - Cliente
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar_web():
    comuna = request.args.get('comuna', '')
    search_query = request.args.get('search', '')
    solo_abiertas = request.args.get('abiertas', 'false')
    
    # Obtener comunas disponibles
    try:
        comunas_response = requests.get(f"{URL_MAESTRA.replace('/farmacias', '')}/farmacias/comunas")
        comunas = comunas_response.json() if comunas_response.status_code == 200 else []
    except:
        comunas = []
    
    farmacias = []
    error = None
    
    if comuna:
        try:
            params = {'comuna': comuna}
            if solo_abiertas == 'true':
                params['abiertas'] = 'true'
            
            response = requests.get(URL_MAESTRA, params=params)
            if response.status_code == 200:
                farmacias = response.json()
                # Filtrar por texto si se proporciona
                if search_query:
                    search_lower = search_query.lower()
                    farmacias = [f for f in farmacias 
                                if search_lower in f.get('nombre', '').lower() 
                                or search_lower in f.get('direccion', '').lower()]
            else:
                error = "Error al consultar farmacias"
        except Exception as e:
            error = f"Error de conexión: {str(e)}"
    
    return render_template('buscar.html', 
                         farmacias=farmacias, 
                         comunas=comunas,
                         comuna_selected=comuna,
                         search_query=search_query,
                         solo_abiertas=solo_abiertas,
                         error=error)

@app.route('/registrar_form')
def registrar_form():
    # Obtener comunas disponibles
    try:
        comunas_response = requests.get(f"{URL_MAESTRA.replace('/farmacias', '')}/farmacias/comunas")
        comunas = comunas_response.json() if comunas_response.status_code == 200 else []
    except:
        comunas = []
    
    return render_template('registrar.html', comunas=comunas)

@app.route('/registrar_web', methods=['POST'])
def registrar_web():
    datos = {
        'local_nombre': request.form['local_nombre'],
        'comuna_nombre': request.form['comuna_nombre'],
        'local_direccion': request.form['local_direccion'],
        'local_telefono': request.form['local_telefono'],
        'funcionamiento_dia': request.form['funcionamiento_dia'],
        'funcionamiento_hora_apertura': request.form['funcionamiento_hora_apertura'] + ':00',
        'funcionamiento_hora_cierre': request.form['funcionamiento_hora_cierre'] + ':00'
    }
    
    # Validar datos básicos
    errores = validar_farmacia_web(datos)
    if errores:
        for error in errores:
            flash(error, 'error')
        # Obtener comunas para el formulario
        try:
            comunas_response = requests.get(f"{URL_MAESTRA.replace('/farmacias', '')}/farmacias/comunas")
            comunas = comunas_response.json() if comunas_response.status_code == 200 else []
        except:
            comunas = []
        return render_template('registrar.html', comunas=comunas, datos=datos)
    
    try:
        response = requests.post(URL_MAESTRA, json=datos)
        if response.status_code == 201:
            flash('Farmacia registrada exitosamente', 'success')
            return redirect(url_for('buscar_web'))
        else:
            result = response.json()
            flash(f"Error al registrar: {result.get('message', 'Error desconocido')}", 'error')
    except Exception as e:
        flash(f"Error de conexión: {str(e)}", 'error')
    
    # Obtener comunas para el formulario
    try:
        comunas_response = requests.get(f"{URL_MAESTRA.replace('/farmacias', '')}/farmacias/comunas")
        comunas = comunas_response.json() if comunas_response.status_code == 200 else []
    except:
        comunas = []
    
    return render_template('registrar.html', comunas=comunas, datos=datos)

def validar_farmacia_web(datos):
    errores = []
    
    # Validar local_nombre
    if not datos.get('local_nombre', '').strip():
        errores.append('El nombre es requerido')
    elif len(datos['local_nombre']) > 255:
        errores.append('El nombre no puede exceder 255 caracteres')
    
    # Validar comuna_nombre
    if not datos.get('comuna_nombre', '').strip():
        errores.append('La comuna es requerida')
    
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
    
    # Validar funcionamiento_dia
    dias_validos = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    dia_semana = datos.get('funcionamiento_dia', '').strip().lower()
    if not dia_semana:
        errores.append('El día de semana es requerido')
    elif dia_semana not in dias_validos:
        errores.append('Día de semana inválido')
    
    # Validar horas
    try:
        apertura = datos.get('funcionamiento_hora_apertura', '').strip()
        cierre = datos.get('funcionamiento_hora_cierre', '').strip()
        
        if not apertura or not cierre:
            errores.append('Las horas de apertura y cierre son requeridas')
        else:
            datetime.strptime(apertura, '%H:%M:%S')
            datetime.strptime(cierre, '%H:%M:%S')
            
            if apertura >= cierre:
                errores.append('La hora de apertura debe ser anterior a la hora de cierre')
                
    except ValueError:
        errores.append('Formato de hora inválido')
    
    return errores

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
