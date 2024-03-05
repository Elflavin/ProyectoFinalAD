from entidades.Departamentos import Departamento
from fireb_init import init
from firebase_admin import db

try:
    init()
except ValueError:
    print("Base de datos ya definido.")



class Empleado:
    ref = db.reference('empleados')
    ref_d = db.reference('departamentos')

    def __init__(self, nombre, appellido, dni, departamento):
        self.nombre = nombre
        self.apellido = appellido
        self.dni = dni
        self.departamento = departamento

    def __repr__(self):
        if self.departamento is None:
            return f"Nombre: {self.nombre, self.apellido} | DNI: {self.dni} | Departamento: 'sin asignar'"
        else:
            return f"Nombre: {self.nombre, self.apellido} | DNI: {self.dni} | Departamento: {self.departamento}"

    @classmethod
    def creEmp(cls, empleado):
        nuevo_empleado = cls(empleado.nombre,empleado.apellido,empleado.dni,empleado.departamento)
        if cls.findRef(nuevo_empleado.dni) is None:
            nuevo_empleado_dict = {
                'nombre': nuevo_empleado.nombre,
                'apellido': nuevo_empleado.apellido,
                'dni': nuevo_empleado.dni,
                'departamento': nuevo_empleado.departamento
            }
            cls.ref.child('empleados').push(nuevo_empleado_dict)
        else:
            return {'status': 'Error', 'message': 'El DNI ya esta en uso'}

    @classmethod
    def getAllEmp(cls):
        tempRef = db.reference("empleados/empleados")
        emps = tempRef.get()

        return emps

    @classmethod
    def delEmp(cls, dni):
        key = cls.findRef(dni)
        cls.ref.child('empleados').child(key).delete()

    @classmethod
    def updEmp(cls, empleado=None, obj=None):
        update_data = {}
        if empleado.nombre is not None:
            update_data['nombre'] = empleado.nombre
        if empleado.apellido is not None:
            update_data['apellido'] = empleado.apellido
        if empleado.dni is not None:
            update_data['dni'] = empleado.dni
        if empleado.departamento is not None:
            update_data['departamento'] = empleado.departamento

        key = cls.findRef(obj)
        cls.ref.child('empleados').child(key).update(update_data)

    @classmethod
    def getEmp(cls, dni):
        key = cls.findRef(dni)
        emp_data = cls.ref.child('empleados').child(key).get()
        if emp_data:
            return cls(
                nombre=emp_data.get('nombre'),
                apellido=emp_data.get('apellido'),
                dni=emp_data.get('dni'),
                departamento=emp_data.get('departamento')
            )
        else:
            return None

    @classmethod
    def findRef(cls, dni):
        empleados = cls.ref.get()
        if empleados is not None:
            for key, empleado in empleados['empleados'].items():
                if 'dni' in empleado and empleado['dni'] == dni:
                    return key
        return None

    @classmethod
    def findRefDep(cls, nombre):
        departamentos = cls.ref_d.get()
        if departamentos is not None:
            for key, departamento in departamentos['departamentos'].items():
                if 'nombre' in departamento and departamento['nombre'] == nombre:
                    return key
        return None

    @classmethod
    def updateEmployee(cls, dni, nuevo_departamento, nuevo_nombre, nuevo_apellido):
        if nuevo_departamento:
            # Crea un objeto Empleado utilizando los datos del formulario
            empleado = cls(
                nombre=nuevo_nombre,
                appellido=nuevo_apellido,
                dni=dni,
                departamento=nuevo_departamento
            )

            # Actualiza el empleado en Firebase
            empleado.updEmp(empleado, dni)

            return empleado

        return None

    @classmethod
    def updatePreviousDepartment(cls, dni, nuevo_departamento):
        empleado = cls.findRef(dni)

        if 'departamento' in empleado and empleado['departamento'] != nuevo_departamento:
            departamento_antiguo = cls.findRefDep(empleado['departamento'])

            if cls.isLeaderOfDepartment(dni, empleado['departamento']):
                cls.setLeaderOfDepartment(departamento_antiguo, "Nadie")

            cls.decreaseEmpCountInDepartment(departamento=departamento_antiguo)

    @classmethod
    def updateNewDepartment(cls, dni, nuevo_departamento):
        if nuevo_departamento:
            # Aumentar en uno el número de empleados en el nuevo departamento
            cls.increaseEmpCountInDepartment(nuevo_departamento)

    # Métodos auxiliares para la actualización del departamento
    @classmethod
    def decreaseEmpCountInDepartment(cls, departamento):
        # Reducir en uno el número de empleados en el departamento
        cls.ref_d.child(departamento).child('n_emp').transaction(
            lambda current_value: current_value - 1 if current_value else 0)

    @classmethod
    def increaseEmpCountInDepartment(cls, departamento):
        # Aumentar en uno el número de empleados en el departamento
        cls.ref_d.child(departamento).child('n_emp').transaction(
            lambda current_value: current_value + 1 if current_value else 1)

    @classmethod
    def isLeaderOfDepartment(cls, dni, departamento):
        # Verificar si el empleado es el líder del departamento
        lider = cls.ref_d.child(departamento).child('lider').get()
        return lider == dni

    @classmethod
    def setLeaderOfDepartment(cls, departamento, nuevo_lider):
        # Establecer el nuevo líder del departamento
        cls.ref_d.child(departamento).update({'lider': nuevo_lider})