from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Configura las credenciales de Firebase
cred = credentials.Certificate("proyectofinalad-af58a-firebase-adminsdk-czuzh-49f852045b.json")
firebase_admin.initialize_app(cred, {
    'https://proyectofinalad-af58a-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Referencia a la base de datos en tiempo real de Firebase
ref = db.reference()

"""
    RUTAS VISTA
"""

@app.route("/", methods=['GET'])
def menu_principal():
    return render_template('index.html')


@app.route("/empleados/VistaCrear", methods=['GET'])
def vista_crear_empleado():
    return render_template('empleado/create_empleado.html')
@app.route("/empleados/VistaBorrar", methods=['GET'])
def vista_borrar_empleado():
    return render_template('empleado/delete_empleado.html')
@app.route("/empleados/VistaModificar", methods=['GET'])
def vista_modificar_empleado():
    return render_template('empleado/update_empleado.html')
@app.route("/empleados/VistaLeer", methods=['GET'])
def vista_crear_empleado():
    return render_template('empleado/read_empleado.html')


@app.route("/departamento/VistaCrear", methods=['GET'])
def vista_crear_departamento():
    return render_template('departamento/create_departamento.html')
@app.route("/departamento/VistaBorrar", methods=['GET'])
def vista_borrar_departamento():
    return render_template('departamento/delete_departamento.html')
@app.route("/departamento/VistaModificar", methods=['GET'])
def vista_modificar_departamento():
    return render_template('departamento/update_departamento.html')
@app.route("/departamento/VistaLeer", methods=['GET'])
def vista_crear_departamento():
    return render_template('departamento/read_departamento.html')



"""
    RUTAS EMPLEADOS
"""


# Rutas para Empleados
@app.route('/empleados', methods=['GET'])
def obtener_empleados():
    empleados = ref.child('empleados').get()
    return jsonify(empleados)


@app.route('/empleados', methods=['POST'])
def agregar_empleado():
    nuevo_empleado = request.get_json()
    ref.child('empleados').push(nuevo_empleado)
    return jsonify({'status': 'OK'})


@app.route('/empleados/<empleado_id>', methods=['DELETE'])
def eliminar_empleado(empleado_id):
    ref.child('empleados').child(empleado_id).delete()
    return jsonify({'status': 'OK'})


# Rutas para actualizar Empleado
@app.route('/empleados/<empleado_id>', methods=['PUT'])
def actualizar_empleado(empleado_id):
    nuevo_empleado = request.get_json()
    ref.child('empleados').child(empleado_id).update(nuevo_empleado)
    return jsonify({'status': 'OK'})

"""
    RUTAS DEPARTAMENTOS
"""


# Rutas para Departamentos
@app.route('/departamentos', methods=['GET'])
def obtener_departamentos():
    departamentos = ref.child('departamentos').get()
    return jsonify(departamentos)


@app.route('/departamentos', methods=['POST'])
def agregar_departamento():
    nuevo_departamento = request.get_json()
    ref.child('departamentos').push(nuevo_departamento)
    return jsonify({'status': 'OK'})


@app.route('/departamentos/<departamento_id>', methods=['DELETE'])
def eliminar_departamento(departamento_id):
    ref.child('departamentos').child(departamento_id).delete()
    return jsonify({'status': 'OK'})


# Rutas para actualizar Departamento
@app.route('/departamentos/<departamento_id>', methods=['PUT'])
def actualizar_departamento(departamento_id):
    nuevo_departamento = request.get_json()
    ref.child('departamentos').child(departamento_id).update(nuevo_departamento)
    return jsonify({'status': 'OK'})


def main():
    app.run(debug=True)
