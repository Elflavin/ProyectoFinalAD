from flask import Flask, request, jsonify, render_template
from entidades.Departamentos import Departamento
from entidades.Empleados import Empleado


# Inicializacion de la aplicacion de Flask
app = Flask(__name__)

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
def vista_bucsar_empleado():
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
def vista_buscar_departamento():
    return render_template('departamento/read_departamento.html')


"""
    RUTAS EMPLEADOS
"""


@app.route('/empleados', methods=['GET'])
def obtener_empleados():
    Empleado.getEmp(request.form['dni'])
    return jsonify({'status': 'OK'})


@app.route('/empleados', methods=['POST'])
def agregar_empleado():
    nuevo_empleado = {
        'nombre': request.form['firstName'],
        'apellido': request.form['lastName'],
        'dni': request.form['dni'],
        'departamento': None
    }
    # Crea un objeto Empleado utilizando los datos del formulario
    empleado = Empleado(**nuevo_empleado)
    empleado.creEmp(empleado)

    return jsonify({'status': 'OK'})


@app.route('/empleados/<empleado_id>', methods=['DELETE'])
def eliminar_empleado():
    Empleado.delEmp(request.form['obj'])
    return jsonify({'status': 'OK'})


# Rutas para actualizar Empleado
@app.route('/empleados/<empleado_id>', methods=['PUT'])
def actualizar_empleado(empleado_id):
    nuevo_empleado = {
        'nombre': request.form['firstName'],
        'apellido': request.form['lastName'],
        'dni': request.form['dni'],
        'departamento': None
    }
    # Crea un objeto Empleado utilizando los datos del formulario
    empleado = Empleado(**nuevo_empleado)
    empleado.updEmp(empleado, request.form['obj'])
    return jsonify({'status': 'OK'})


"""
    RUTAS DEPARTAMENTOS
"""


@app.route('/departamentos', methods=['GET'])
def obtener_departamentos():
    Departamento.getDep(request.form['name'])
    return jsonify({'status': 'OK'})


@app.route('/departamentos', methods=['POST'])
def agregar_departamento():
    nuevo_departamento = {
        'nombre': request.form['name'],
        'desc': request.form['desc'],
        'lider': None,
        'n_emp': 0
    }
    Departamento.creDep(**nuevo_departamento)
    return jsonify({'status': 'OK'})


@app.route('/departamentos/<departamento_id>', methods=['DELETE'])
def eliminar_departamento():
    Departamento.delDep(request.form['name'])
    return jsonify({'status': 'OK'})


# Rutas para actualizar Departamento
@app.route('/departamentos/<departamento_id>', methods=['PUT'])
def actualizar_departamento():
    nuevo_departamento = {
        'nombre': request.form['name'],
        'desc': request.form['desc'],
        'lider': request.form['lider'],
        'n_emp': None
    }
    departamento = Departamento(**nuevo_departamento)
    Departamento.updDep(departamento, request.form['obj'])
    return jsonify({'status': 'OK'})


def main():
    app.run(debug=True)
