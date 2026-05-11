from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import requests
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = '1231234'

# REEMPLAZA CON LA IP PRIVADA O PÚBLICA DE LA INSTANCIA 1
URL_MAESTRA = "http://32.197.236.185/Farmacias_api.php"

# API Endpoints
@app.route('/consultar', methods=['GET'])
def consultar():
    comuna = request.args.get('comuna')
    abiertas = request.args.get('abiertas', 'false')
    
    # Redirige la consulta a la Instancia 1
    response = requests.get(URL_MAESTRA, params={'comuna': comuna, 'abiertas': abiertas}, timeout=10)
    
    return jsonify(response.json()), response.status_code

@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    try:
        # Obtener todas las farmacias
        response = requests.get(URL_MAESTRA, timeout=10)
        if response.status_code == 200:
            farmacias = response.json()
            
            # Calcular estadísticas
            # Usar zona horaria de Chile (Santiago)
            tz_chile = pytz.timezone('America/Santiago')
            ahora = datetime.now(tz_chile)
            dia_semana_map = {
                0: 'domingo', 1: 'lunes', 2: 'martes', 3: 'miercoles',
                4: 'jueves', 5: 'viernes', 6: 'sabado'
            }
            dia_nombre = dia_semana_map[ahora.weekday()]
            hora_actual = ahora.strftime('%H:%M:%S')
            
            abiertas_ahora = 0
            cerradas_ahora = 0
            
            for farmacia in farmacias:
                if farmacia.get('funcionamiento_dia') == dia_nombre:
                    apertura = farmacia.get('funcionamiento_hora_apertura', '')
                    cierre = farmacia.get('funcionamiento_hora_cierre', '')
                    
                    if apertura <= hora_actual <= cierre:
                        abiertas_ahora += 1
                    else:
                        cerradas_ahora += 1
                else:
                    cerradas_ahora += 1
            
            return jsonify({
                'abiertas_ahora': abiertas_ahora,
                'cerradas_ahora': cerradas_ahora,
                'total_farmacias': len(farmacias),
                'hora_actual': hora_actual
            })
        else:
            return jsonify({'error': 'No se pudieron obtener las farmacias'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/registrar', methods=['POST'])
def registrar():
    # Recibe datos del cliente y los manda a la Instancia 1
    datos = request.json
    response = requests.post(URL_MAESTRA, json=datos, timeout=10)
    
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
    
    # Obtener comunas disponibles (con timeout)
    try:
        comunas_response = requests.get(f"{URL_MAESTRA}?comunas=true", timeout=5)
        if comunas_response.status_code == 200:
            # La API ya devuelve lista de comunas únicas
            comunas = comunas_response.json()
            comunas = sorted(comunas) if comunas else []
        else:
            comunas = []
    except requests.exceptions.Timeout:
        comunas = []
    except Exception as e:
        print(f"Error obteniendo comunas: {e}")
        comunas = []
    
    farmacias = []
    error = None
    
    # Siempre obtener farmacias cuando hay búsqueda o filtros
    if search_query or solo_abiertas == 'true':
        try:
            params = {}
            if comuna:
                params['comuna'] = comuna
            if solo_abiertas == 'true':
                params['abiertas'] = 'true'
            
            response = requests.get(URL_MAESTRA, params=params, timeout=10)
            if response.status_code == 200:
                farmacias = response.json()
                # Filtrar por texto si se proporciona
                if search_query:
                    search_lower = search_query.lower()
                    # Buscar en nombre, dirección O comuna
                    farmacias = [f for f in farmacias 
                                if search_lower in f.get('local_nombre', '').lower() 
                                or search_lower in f.get('local_direccion', '').lower()
                                or search_lower in f.get('comuna_nombre', '').lower()]
            else:
                error = "Error al consultar farmacias"
        except Exception as e:
            error = f"Error de conexión: {str(e)}"
    elif not comuna and not search_query and solo_abiertas == 'false':
        try:
            response = requests.get(URL_MAESTRA, timeout=10)
            if response.status_code == 200:
                farmacias = response.json()
            else:
                error = "Error al consultar farmacias"
        except Exception as e:
            error = f"Error de conexión: {str(e)}"
    else:
        # Si hay comuna seleccionada pero no búsqueda de texto ni filtro de abiertas
        try:
            params = {}
            if comuna:
                params['comuna'] = comuna
            
            response = requests.get(URL_MAESTRA, params=params, timeout=10)
            if response.status_code == 200:
                farmacias = response.json()
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
    # Obtener comunas disponibles (con timeout)
    try:
        comunas_response = requests.get(f"{URL_MAESTRA}?comunas=true", timeout=5)
        if comunas_response.status_code == 200:
            # La API ya devuelve lista de comunas únicas
            comunas = comunas_response.json()
            comunas = sorted(comunas) if comunas else []
        else:
            comunas = []
    except requests.exceptions.Timeout:
        comunas = []
    except Exception as e:
        print(f"Error obteniendo comunas: {e}")
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
            comunas_response = requests.get(f"{URL_MAESTRA}?comunas=true", timeout=5)
            if comunas_response.status_code == 200:
                # La API ya devuelve lista de comunas únicas
                comunas = comunas_response.json()
                comunas = sorted(comunas) if comunas else []
            else:
                comunas = []
        except requests.exceptions.Timeout:
            comunas = []
        except Exception as e:
            print(f"Error obteniendo comunas en error: {e}")
            comunas = []
        return render_template('registrar.html', comunas=comunas, datos=datos)
    
    try:
        print(f"=== INICIANDO REGISTRO ===")
        print(f"URL_MAESTRA: {URL_MAESTRA}")
        print(f"Datos a enviar: {datos}")
        print(f"Headers: Content-Type: application/json")
        
        response = requests.post(URL_MAESTRA, json=datos, timeout=10)
        
        print(f"=== RESPUESTA SERVIDOR ===")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        print(f"Response Length: {len(response.text)} caracteres")
        
        # Intentar parsear JSON
        try:
            response_json = response.json()
            print(f"Response JSON: {response_json}")
        except:
            print("Response no es JSON válido")
            response_json = None
        
        if response.status_code == 201:
            print("✅ REGISTRO EXITOSO")
            flash('Farmacia registrada exitosamente', 'success')
            return redirect(url_for('buscar_web'))
        else:
            print("❌ ERROR EN REGISTRO")
            if response_json:
                error_msg = response_json.get('message', response_json.get('error', 'Error desconocido'))
                print(f"Error desde API (JSON): {error_msg}")
                flash(f"Error al registrar: {error_msg}", 'error')
            else:
                print(f"Error desde API (texto): {response.text}")
                flash(f"Error al registrar: {response.text}", 'error')
                
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - El servidor maestro no responde en 10 segundos")
        flash('Error: Timeout al conectar con el servidor maestro', 'error')
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR - No se puede conectar al servidor maestro")
        flash('Error: No se puede conectar con el servidor maestro', 'error')
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR - Error en la petición: {e}")
        flash(f'Error en la petición: {e}', 'error')
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        flash(f'Error inesperado: {e}', 'error')
    
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
    app.run(host='0.0.0.0', port=80, debug=False)
